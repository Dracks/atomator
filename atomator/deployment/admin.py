# Django imports
from django.contrib import admin

from .models import ConfigEnvironment, DeploymentConfiguration, Machine, Tag


class ConfigEnvironmentInline(admin.TabularInline):
    model = ConfigEnvironment


@admin.register(DeploymentConfiguration)
class DeployConfigurationInlines(admin.ModelAdmin):
    filter_horizontal = ('tags_list', )
    inlines = [ConfigEnvironmentInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    pass
