# Django imports
from django.contrib import admin

# Other libraries
import nested_admin

from .models import (
    Application,
    RepoApp,
    RepoAppIntValue,
    RepoAppStringValue,
    RepoAppTextValue,
    Repository,
    RepositoryIntValue,
    RepositoryStringValue,
    RepositoryTextValue,
    Token,
)


class TokenInline(nested_admin.NestedTabularInline):
    model = Token
    extra = 0


class RepositoryIntValuesInline(admin.TabularInline):
    model = RepositoryIntValue
    extra = 1


class RepositoryStringValuesInline(admin.TabularInline):
    model = RepositoryStringValue
    extra = 1


class RepositoryTextValuesInline(admin.TabularInline):
    model = RepositoryTextValue
    extra = 1


class RepositoryAdmin(admin.ModelAdmin):
    inlines = [
        RepositoryIntValuesInline,
        RepositoryStringValuesInline,
        RepositoryTextValuesInline,
    ]
    list_display = ("provider", "name", "url")


class RepoAppIntValuesInline(nested_admin.NestedTabularInline):
    model = RepoAppIntValue
    extra = 1


class RepoAppStringValuesInline(nested_admin.NestedTabularInline):
    model = RepoAppStringValue
    extra = 1


class RepoAppTextValuesInline(nested_admin.NestedTabularInline):
    model = RepoAppTextValue
    extra = 1


class RepoAppInline(nested_admin.NestedStackedInline):
    model = RepoApp
    inlines = [
        RepoAppIntValuesInline,
        RepoAppStringValuesInline,
        RepoAppTextValuesInline,
    ]
    extra = 0


class ApplicationAdmin(nested_admin.NestedModelAdmin):
    model = Application
    inlines = [TokenInline, RepoAppInline]


@admin.register(RepoApp)
class RepoAppAdmin(admin.ModelAdmin):
    inlines = [
        RepoAppIntValuesInline,
        RepoAppStringValuesInline,
        RepoAppTextValuesInline,
    ]


admin.site.register(Application, ApplicationAdmin)
admin.site.register(Repository, RepositoryAdmin)
