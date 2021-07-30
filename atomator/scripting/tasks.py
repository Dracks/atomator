# Standard Library
import os

# Other libraries
from celery import shared_task
# Django imports
from django.conf import settings
from django.db.models import signals
from django.dispatch import receiver

from .models import ScriptFile, ScriptFileType, ScriptsProvider


@shared_task
def inspect_data(script_provider_id):
    provider = ScriptsProvider.objects.get(id=script_provider_id)
    old_files = list(
        ScriptFile.objects.filter(provider=provider).values_list("name", flat=True)
    )
    path = provider.get_full_path()
    excluded_list = provider.exclude_path_set.values_list("path", flat=True)

    path_size = len(path) + 1

    for root, subdirs, files in os.walk(path):
        excluded_match = [
            excluded
            for excluded in excluded_list
            if root[path_size:].startswith(excluded)
        ]

        if len(excluded_match) == 0:
            for filename in files:
                ext = os.path.splitext(filename)[1]
                complete_path = "{}/{}".format(root, filename)
                relative_path = complete_path[path_size:]

                if relative_path in old_files:
                    idx = old_files.index(relative_path)
                    del old_files[idx]

                qs = ScriptFile.objects.filter(provider=provider, name=relative_path)
                if qs.count() == 0:
                    type = ScriptFileType.unknown
                    if ext == ".yaml" or ext == ".yml":
                        type = ScriptFileType.ansible
                    elif ext == ".ini":
                        type = ScriptFileType.inventory
                    ScriptFile.objects.create(
                        provider=provider, type=type, name=relative_path
                    )
    for to_delete in old_files:
        ScriptFile.objects.filter(provider=provider, name=to_delete).all().delete()
