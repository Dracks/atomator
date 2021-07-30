# Django imports
from django.db import models

# Atom platform
from atomator.application.models import Application
from atomator.scripting.models import ScriptFile, ScriptsProvider
# Create your models here.
from atomator.version_manager.models import Build


class EnvironmentChoices(models.IntegerChoices):
    devel = 0, "Development"
    preprod = 1, "Staging"
    production = 2, "Production"


HASH_ENVIRONMENTS = {value: label for value, label in EnvironmentChoices.choices}


class TaskStatusChoices(models.IntegerChoices):
    nothing = 0, "Nothing done"
    changed = 1, "Changed"
    error = 2, "Error"
    unreachable = 3, "Unreachable"


HASH_TASK_STATUS = {value: label for value, label in TaskStatusChoices.choices}


class OutputChoices(models.IntegerChoices):
    pending = -1, "Pending"
    working = 0, "Working"
    ok = 1, "OK"
    error = 2, "Error"


HASH_OUTPUT_CHOICES = {value: label for value, label in OutputChoices.choices}


class AbstractConfig(models.Model):
    key = models.CharField(max_length=255)
    config = models.CharField(max_length=255)
    is_secret = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Machine(models.Model):
    services_installed_list = models.ManyToManyField(Build)
    environment = models.SmallIntegerField(choices=EnvironmentChoices.choices)
    name = models.CharField(max_length=255)


# To Do:
# Application - should have his configurations
# Application - Environment should have configuration
# Machine - should have have configurations?


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class DeploymentConfiguration(models.Model):
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, related_name="configurations_set"
    )
    name = models.CharField(max_length=255)
    provider = models.ForeignKey(ScriptsProvider, on_delete=models.PROTECT)
    script = models.ForeignKey(ScriptFile, on_delete=models.PROTECT, related_name="+")
    tags_list = models.ManyToManyField(Tag, related_name="+", blank=True)

    def __str__(self):
        return self.name


class ConfigEnvironment(models.Model):
    environment = models.SmallIntegerField(choices=EnvironmentChoices.choices)
    configuration = models.ForeignKey(
        DeploymentConfiguration, on_delete=models.CASCADE, related_name="environments"
    )
    inventory = models.ForeignKey(
        ScriptFile, on_delete=models.PROTECT, related_name="+"
    )

    def __str__(self):
        return HASH_ENVIRONMENTS[self.environment]

    @property
    def name(self):
        return HASH_ENVIRONMENTS[self.environment]


class ExecutionOutput(models.Model):
    status = models.SmallIntegerField(choices=OutputChoices.choices)
    environment = models.ForeignKey(ConfigEnvironment, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    build = models.ForeignKey(
        Build, on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )
    application = models.ForeignKey(
        Application, on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )

    class Meta:
        ordering = ("-date",)


class ExecutionError(models.Model):
    execution = models.OneToOneField(
        ExecutionOutput, on_delete=models.CASCADE, related_name="error"
    )
    message = models.CharField(max_length=255)
    stacktrace = models.TextField()


class TaskOutput(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    execution = models.ForeignKey(ExecutionOutput, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    status = models.SmallIntegerField(choices=TaskStatusChoices.choices)
    stdout = models.TextField(null=True, blank=True)
    stderr = models.TextField(null=True, blank=True)
    message = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ("-id",)
