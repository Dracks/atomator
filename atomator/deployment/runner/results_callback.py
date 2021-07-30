# Other libraries
from ansible.plugins.callback import CallbackBase

from ..models import Machine, TaskOutput, TaskStatusChoices


class ResultCallback(CallbackBase):
    def __init__(self, deployment_output):
        super(ResultCallback, self).__init__()
        self.deployment_output = deployment_output

    """A sample callback plugin used for performing an action as results come in

    If you want to collect all results into a single object for processing at
    the end of the execution, look into utilizing the ``json`` callback plugin
    or writing your own custom callback plugin
    """

    def update_machine(self, host_name):
        environment = self.deployment_output.environment.environment
        qs = Machine.objects.filter(environment=environment, name=host_name)
        if qs.exists():
            return qs.first()
        else:
            return Machine.objects.create(environment=environment, name=host_name)

    def save_record(self, result, is_failed=False):
        host_name = result._host.get_name()
        machine = self.update_machine(host_name)
        status = TaskStatusChoices.nothing

        if is_failed or result.is_failed():
            status = TaskStatusChoices.error
        elif result.is_changed():
            status = TaskStatusChoices.changed

        TaskOutput.objects.create(
            machine=machine,
            execution=self.deployment_output,
            name=result.task_name,
            status=status,
            stdout=result._result.get("stdout", ""),
            stderr=result._result.get("stderr", ""),
            message=result._result.get("msg", ""),
        )

    def v2_runner_on_failed(self, result, ignore_errors=False):
        self.save_record(result, is_failed=True)

    def v2_runner_on_ok(self, result, **kwargs):
        self.save_record(result)

    def v2_runner_on_unreachable(self, result):
        host_name = result._host.get_name()
        machine = self.update_machine(host_name)

        TaskOutput.objects.create(
            machine=machine,
            execution=self.deployment_output,
            name=result.task_name,
            status=TaskStatusChoices.unreachable,
            message=result._result.get("msg", ""),
        )