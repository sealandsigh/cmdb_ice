# -*- coding: utf-8 -*-
# __author__="jiajun.zhu"
# DATE:2019/7/16

import json
import shutil
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
import ansible.constants as C


class ResultCallback(CallbackBase):
    def v2_runner_on_ok(self, result, **kwargs):
        host = result._host
        print(result.task_name)
        print(json.dumps({host.name: result._result}, indent=4))

# since API is constructed for CLI it expects certain options to always be set, named tuple 'fakes' the args parsing options object
Options = namedtuple('Options', ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user', 'check', 'diff'])
options = Options(connection='local', module_path=[], forks=10, become=None, become_method=None, become_user=None, check=False, diff=False)

# initialize needed objects
loader = DataLoader() # Takes care of finding and reading yaml, json and ini files
passwords = {}

# Instantiate our ResultCallback for handling results as they come in. Ansible expects this to be one of its main display outlets
results_callback = ResultCallback()

# create inventory, use path to host config file as source or hosts in a comma separated string
inventory = InventoryManager(loader=loader, sources='hosts')        #剧本位置

# variable manager takes care of merging all the different sources to give you a unifed view of variables available in each context
variable_manager = VariableManager(loader=loader, inventory=inventory)

# create datastructure that represents our play, including tasks, this is basically what our YAML loader does internally.
play_source =  {
        'name' : "test",
        'hosts' : 'all',        #在哪些主机上执行
        'gather_facts' : 'no',
        'tasks' : [             #任务列表
            {
                'name': 'fact', #任务名称
                'setup':''      #执行模块
            }
         ]
    }

# Create play object, playbook objects use .load instead of init or new methods,
# this will also automatically create the task objects from the info provided in play_source
play = Play().load(play_source, variable_manager=variable_manager, loader=loader)

# Run it - instantiate task queue manager, which takes care of forking and setting up all objects to iterate over host list and tasks
tqm = None
try:
    tqm = TaskQueueManager(
              inventory=inventory,
              variable_manager=variable_manager,
              loader=loader,
              options=options,
              passwords=passwords,
              stdout_callback=results_callback,  # Use our custom callback instead of the ``default`` callback plugin, which prints to stdout
          )
    result = tqm.run(play) # most interesting data for a play is actually sent to the callback's methods
finally:
    # we always need to cleanup child procs and the structres we use to communicate with them
    if tqm is not None:
        tqm.cleanup()

    # Remove ansible tmpdir
    shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)