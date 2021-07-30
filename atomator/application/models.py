# Standard Library
import uuid

# Django imports
from django.db import models
from django.dispatch import Signal, receiver

from .repository import GitlabRepository

new_release = Signal(providing_args=["application", "build"])


@receiver(new_release)
def on_new_released(sender, application, build, **kwargs):
    # Todo update changes / release notes
    rep_list = application.repository_set.all()
    for rep in rep_list:
        if rep.provider == ProviderChoices.gitlab:
            gitlab = GitlabRepository(application, rep)
            gitlab.create_tag(build.tag_name(), build.commit)


# Create your models here.
class ProviderChoices(models.IntegerChoices):
    gitlab = 0, "Gitlab"


class Application(models.Model):
    name = models.CharField(max_length=255)
    release_branch = models.CharField(max_length=50, default="main")

    def __str__(self):
        return self.name


class Token(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    token = models.CharField(max_length=255, blank=True, unique=True)

    def save(self):
        if not self.token:
            self.token = uuid.uuid4()
        return super(Token, self).save()


# TAG API: https://docs.gitlab.com/ee/api/tags.html
# project access token: https://docs.gitlab.com/ee/user/project/settings/project_access_tokens.html
class Repository(models.Model):
    applications = models.ManyToManyField(Application, through="RepoApp")
    provider = models.SmallIntegerField(choices=ProviderChoices.choices)
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Repositories"


class RepoApp(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)


class RepositoryIntValue(models.Model):
    repository = models.ForeignKey(
        Repository, models.CASCADE, related_name="extra_int_set"
    )
    key = models.CharField(max_length=55)
    value = models.IntegerField()

    class Meta:
        indexes = [models.Index(fields=["repository", "key"])]


class RepositoryStringValue(models.Model):
    repository = models.ForeignKey(
        Repository, models.CASCADE, related_name="extra_string_set"
    )
    key = models.CharField(max_length=55)
    value = models.CharField(max_length=255)

    class Meta:
        indexes = [models.Index(fields=["repository", "key"])]


class RepositoryTextValue(models.Model):
    repository = models.ForeignKey(
        Repository, models.CASCADE, related_name="extra_text_set"
    )
    key = models.CharField(max_length=55)
    value = models.TextField()

    class Meta:
        indexes = [models.Index(fields=["repository", "key"])]


class RepoAppIntValue(models.Model):
    repo_app = models.ForeignKey(RepoApp, models.CASCADE, related_name="extra_int_set")
    key = models.CharField(max_length=55)
    value = models.IntegerField()

    class Meta:
        indexes = [models.Index(fields=["repo_app", "key"])]


class RepoAppStringValue(models.Model):
    repo_app = models.ForeignKey(
        RepoApp, models.CASCADE, related_name="extra_string_set"
    )
    key = models.CharField(max_length=55)
    value = models.CharField(max_length=255)

    class Meta:
        indexes = [models.Index(fields=["repo_app", "key"])]


class RepoAppTextValue(models.Model):
    repo_app = models.ForeignKey(RepoApp, models.CASCADE, related_name="extra_text_set")
    key = models.CharField(max_length=55)
    value = models.TextField()

    class Meta:
        indexes = [models.Index(fields=["repo_app", "key"])]
