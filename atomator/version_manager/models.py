# Standard Library
import uuid

# Django imports
from django.core.files.storage import default_storage
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

# Atom platform
from atomator.application.models import Application, new_release


class ChangesChoices(models.IntegerChoices):
    major = 0, "Major"
    minor = 1, "Minor"
    patch = 2, "Patch"


class Build(models.Model):
    application = models.ForeignKey(Application, models.PROTECT)
    date = models.DateTimeField(auto_now_add=True)
    major = models.PositiveIntegerField()
    minor = models.PositiveIntegerField()
    patch = models.PositiveIntegerField()
    commit = models.CharField(max_length=255)
    branch = models.CharField(max_length=255, default="main")
    release = models.BooleanField(default=False)
    change = models.IntegerField(choices=ChangesChoices.choices)

    __original_release = None

    def __init__(self, *args, **kwargs):
        super(Build, self).__init__(*args, **kwargs)
        self.__original_release = self.release

    def tag_name(self):
        return f"{self.major}.{self.minor}.{self.patch}"

    def save(self, *args, **kwargs):

        if self.release and not self.__original_release:
            if self.branch != self.application.release_branch:
                raise Exception(
                    f"Cannot do release on branch {self.branch} please do release in {self.application.release_branch}"
                )
            new_release.send(Build, application=self.application, build=self)
            list_previous = Build.objects.filter(
                application=self.application, date__lt=self.date, release=False
            )
            for prev_build in list_previous:
                for change in prev_build.changes_list.all():
                    change.build = self
                    change.save()
                prev_build.delete()
        return super(Build, self).save(*args, **kwargs)

    class Meta:
        ordering = ("-date",)
        indexes = [
            models.Index(fields=["major", "minor"]),
        ]


class FileInfo(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)
    build = models.OneToOneField(Build, related_name="file", on_delete=models.CASCADE)
    size = models.PositiveIntegerField()
    file_name = models.CharField(max_length=256)
    content_type = models.CharField(max_length=256)

    class Meta:
        indexes = [models.Index(fields=["uuid"])]


class Change(models.Model):
    class ChangeType(models.TextChoices):
        FIX = "fix", "Fix"
        IMPROVEMENT = "imp", "Improvement"
        NEW_FEATURE = "fea", "New Feature"
        UNKNOWN = "unk", "Unknown"

    build = models.ForeignKey(
        Build, on_delete=models.PROTECT, related_name="changes_list"
    )
    type = models.CharField(
        max_length=3, choices=ChangeType.choices, null=True, blank=True
    )
    description = models.TextField()


@receiver(pre_delete, sender=FileInfo)
def on_file_delete(sender, instance, **kwargs):
    default_storage.delete(instance.file_name)
