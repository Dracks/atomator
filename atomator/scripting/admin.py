# Django imports
from django.contrib import admin

# Register your models here.
from .models import ExcludedPath, ScriptFile, ScriptsProvider


class ScriptFileInline(admin.TabularInline):
    model = ScriptFile
    extra = 0


class ExcludedPathInline(admin.TabularInline):
    model = ExcludedPath


@admin.register(ScriptsProvider)
class ScriptsProviderAdmin(admin.ModelAdmin):
    inlines = [ExcludedPathInline, ScriptFileInline]
