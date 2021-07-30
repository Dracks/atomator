# Standard Library
import json

# Django imports
from django.core.management.base import BaseCommand

# Other libraries
from ansible.plugins.callback import CallbackBase

# Atom platform
from atomator.deployment.runner.execute_playbook import execute_playbook


class ResultCallback(CallbackBase):
    """A sample callback plugin used for performing an action as results come in

    If you want to collect all results into a single object for processing at
    the end of the execution, look into utilizing the ``json`` callback plugin
    or writing your own custom callback plugin
    """

    def v2_runner_on_failed(self, result, ignore_errors=False):
        host = result._host
        print(
            json.dumps(
                {
                    host.name: {
                        "name": result.task_name,
                        "is_failed": True,
                        "is_changed": result.is_changed(),
                        "stdout": result._result.get("stdout_lines", []),
                        "stderr": result._result.get("stderr_lines", []),
                        "message": result._result.get("msg", "").split("\n"),
                    }
                },
                indent=4,
            )
        )

    def v2_runner_on_ok(self, result, **kwargs):
        """Print a json representation of the result

        This method could store the result in an instance attribute for retrieval later
        """
        host = result._host
        print(
            json.dumps(
                {
                    host.name: {
                        "name": result.task_name,
                        "is_failed": result.is_failed(),
                        "is_changed": result.is_changed(),
                        "stdout": result._result.get("stdout_lines", []),
                        "stderr": result._result.get("stderr_lines", []),
                        "message": result._result.get("msg", "").split("\n"),
                    }
                },
                indent=4,
            )
        )

        # print(json.dumps({host.name: result._result}, indent=4))


class Command(BaseCommand):
    def handle(self, *args, **options):
        results_callback = ResultCallback()
        execute_playbook(
            "test",
            "artifact_file",
            "test-files/main.yaml",
            "test-files/ansible.ini",
            ["tag-all", "peperoni"],
            results_callback,
        )
