# Standard Library
import os
from subprocess import Popen, PIPE, TimeoutExpired
import time
import sys

import logging

# Other libraries
from celery import shared_task
import time

# Django imports
from django.conf import settings

from .models import ExecutionOutput, OutputChoices
from .runner.execute_playbook import execute_playbook
from .runner.results_callback import ResultCallback

logger = logging.getLogger()

@shared_task
def start_deployment(output_deploy_id):
    command = [sys.executable, "manage.py",  "deploy", str(output_deploy_id)]
    proc = Popen(command, stdout=PIPE, stderr=PIPE, env=os.environ)
    time.sleep(10)
    stderr = proc.stderr.read()
    if (stderr):
        logger.error(stderr)