#!/usr/bin/env python
# Standard Library
import os
import shutil

# Other libraries
import ansible.constants as C
from ansible import context
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.inventory.manager import InventoryManager
from ansible.module_utils.common.collections import ImmutableDict
from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play import Play
from ansible.vars.manager import VariableManager
from django.conf import settings


def load_playbook(loader, playbook_file):
    loaded_file = []
    base_path = os.path.dirname(playbook_file)
    for playbook in loader.load_from_file(playbook_file):
        import_playbook = playbook.get("import_playbook", None)
        if import_playbook:
            loaded_file.extend(
                load_playbook(loader, os.path.join(base_path, import_playbook))
            )
        else:
            loaded_file.append(playbook)
    return loaded_file


def execute_playbook(
    custom_vars, playbook_file, inventory_file, tags_list, results_callback
):
    # since the API is constructed for CLI it expects certain options to always be set in the context object
    context.CLIARGS = ImmutableDict(
        connection="ssh",
        module_path=[settings.BASE_DIR],
        forks=10,
        become=None,
        become_method=None,
        become_user=None,
        check=False,
        diff=False,
        syntax=False,
        start_at_task=None,
        verbosity=3,
        tags=tags_list
    )

    # initialize needed objects
    loader = DataLoader()  # Takes care of finding and reading yaml, json and ini files
    passwords = dict(vault_pass="secret")

    # create inventory, use path to host config file as source or hosts in a comma separated string
    # Aqui podem cridar al fitxer directament
    inventory = InventoryManager(loader=loader, sources=inventory_file)

    # variable manager takes care of merging all the different sources to give you a unified view of variables available in each context
    variable_manager = VariableManager(loader=loader, inventory=inventory)

    # create data structure that represents our play, including tasks, this is basically what our YAML loader does internally.
    # Carregar amb pyyalm, espero que funcioni a la primera
    """play_source =  dict(
            name = "Ansible Play",
            hosts = 'localhost',
            gather_facts = 'no',
            tasks = [
                dict(action=dict(module='shell', args='ls'), register='shell_out'),
                dict(action=dict(module='debug', args=dict(msg='{{shell_out.stdout}}')))
            ]
        )
    """

    # Create play object, playbook objects use .load instead of init or new methods,
    # this will also automatically create the task objects from the info provided in play_source
    playbook_list = [
        {
            **playbook,
            "tasks": [
                task
                for task in playbook.get("tasks", [])
                if len(tags_list) == 0
                or any(tag in tags_list for tag in task.get("tags", []))
                or any(tag in tags_list for tag in playbook.get("tags", []))
            ],
        }
        for playbook in load_playbook(loader, playbook_file)
    ]

    play_list = [
        Play().load(
            playbook,
            variable_manager=variable_manager,
            loader=loader,
            vars=custom_vars,
        )
        for playbook in playbook_list
    ]

    # Run it - instantiate task queue manager, which takes care of forking and setting up all objects to iterate over host list and tasks
    tqm = None
    try:
        tqm = TaskQueueManager(
            inventory=inventory,
            variable_manager=variable_manager,
            loader=loader,
            passwords=passwords,
            # Use our custom callback instead of the ``default`` callback plugin, which prints to stdout
            stdout_callback=results_callback,
        )
        results = [
            # most interesting data for a play is actually sent to the callback's methods
            tqm.run(play)
            for play in play_list
        ]
    finally:
        # we always need to cleanup child procs and the structures we use to communicate with them
        if tqm is not None:
            tqm.cleanup()

        # Remove ansible tmpdir
        shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)
    return results
