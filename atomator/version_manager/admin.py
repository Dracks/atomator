# Django imports
from django.contrib import admin

from .models import Build, Change, FileInfo


class ChangeInline(admin.StackedInline):
    model = Change
    extra = 3


class FileInfo(admin.StackedInline):
    model = FileInfo
    extra = 0


class BuildAdmin(admin.ModelAdmin):
    model = Build
    list_display = ("date", "application", "major", "minor", "patch", "release")
    inlines = [ChangeInline, FileInfo]


admin.site.register(Build, BuildAdmin)
