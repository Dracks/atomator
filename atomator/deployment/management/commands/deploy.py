# Standard Library
import logging
import os
import traceback

# Django imports
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand

# Other libraries
from ansible.plugins.callback import CallbackBase

# Atom platform
from atomator.deployment.models import ExecutionError, ExecutionOutput, OutputChoices
from atomator.deployment.runner.execute_playbook import execute_playbook
from atomator.deployment.runner.results_callback import ResultCallback

logger = logging.getLogger()


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("output_deploy_id")

    def handle(self, *args, **options):
        deploy_id = options["output_deploy_id"]
        logger.info(f"Start deploy {deploy_id}")
        output_exec = ExecutionOutput.objects.get(
            id=deploy_id, status=OutputChoices.pending
        )
        output_exec.status = OutputChoices.working
        output_exec.save()
        try:

            environment_info = output_exec.environment
            deployment_config = environment_info.configuration
            playbook_file = deployment_config.script.get_full_path()
            inventory_file = environment_info.inventory.get_full_path()
            tags_list = [tag.name for tag in deployment_config.tags_list.all()]
            build_info = output_exec.build
            artifact_path = default_storage.path(build_info.file.file_name)
            results_callback = ResultCallback(output_exec)
            execute_playbook(
                {
                    "env_name": environment_info.name,
                    "artifact_file": artifact_path,
                    "application_name": build_info.application.name,
                    "deploy_version": {
                        "tag": build_info.tag_name(),
                        "date": build_info.date,
                        "release": build_info.release,
                    },
                },
                playbook_file,
                inventory_file,
                tags_list,
                results_callback,
            )
            output_exec.status = OutputChoices.ok
            logger.info(f"Ended deploy {deploy_id}")
        except Exception as e:
            ExecutionError.objects.create(
                execution=output_exec,
                message=str(e)[:255],
                stacktrace=traceback.format_exc(),
            )
            output_exec.status = OutputChoices.error
        output_exec.save()
