# Standard Library
import os

# Other libraries
import celery
# Django imports
from django.conf import settings
from django.db import models


class ScriptFileType(models.IntegerChoices):
    unknown = 0, "Unknown"
    ansible = 1, "Ansible Script"
    inventory = 2, "Inventory File"


# For use with git
# on New GitPython repo.clone_from_url(...)
# code = models.CharField(max_length=50)
# repo_url = models.CharField(max_length=255)


class ScriptsProvider(models.Model):
    name = models.CharField(max_length=255)
    folder = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def get_full_path(self):
        return os.path.join(settings.PROVIDERS_SCRIPT_ROOT, self.folder)

    def save(self, *args, **kwargs):
        instance = super(ScriptsProvider, self).save(*args, **kwargs)
        celery.current_app.send_task(
            "atomator.scripting.tasks.inspect_data", (self.id,)
        )
        return instance


class ExcludedPath(models.Model):
    provider = models.ForeignKey(
        ScriptsProvider, on_delete=models.CASCADE, related_name="exclude_path_set"
    )
    path = models.CharField(max_length=255)


class ScriptFile(models.Model):
    provider = models.ForeignKey(ScriptsProvider, on_delete=models.CASCADE)
    type = models.SmallIntegerField(choices=ScriptFileType.choices)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def get_full_path(self):
        return os.path.join(self.provider.get_full_path(), self.name)

    class Meta:
        indexes = [
            models.Index(fields=["name"], name="name_idx"),
        ]


class Tags(models.Model):
    name = models.CharField(max_length=255)
    file = models.ManyToManyField(ScriptFile, related_name="ScriptFile")
