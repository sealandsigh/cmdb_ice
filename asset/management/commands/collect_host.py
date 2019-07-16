# -*- coding: utf-8 -*-
# __author__="jiajun.zhu"
# DATE:2019/7/15

import shutil
import ansible.constants as C
import os

from django.core.management import BaseCommand
from django.conf import settings

from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase


class ResultCallback(CallbackBase):
    def v2_runner_on_ok(self, result, **kwargs):
        print(result._host)
        print(result.task_name)

class Command(BaseCommand):

    def handle(self,*args,**options):
        print('test')
        Options = namedtuple('Options',
                             ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user', 'check',
                              'diff'])
        options = Options(connection='local', module_path=[], forks=10, become=None, become_method=None,
                          become_user=None, check=False, diff=False)

        loader = DataLoader()  # Takes care of finding and reading yaml, json and ini files
        passwords = {}
        results_callback = ResultCallback()
        inventory = InventoryManager(loader=loader, sources=os.path.join(settings.BASE_DIR,"etc","hosts"))  # 剧本位置
        variable_manager = VariableManager(loader=loader, inventory=inventory)

        play_source = {
            'name': "test",
            'hosts': 'all',  # 在哪些主机上执行
            'gather_facts': 'no',
            'tasks': [  # 任务列表
                {
                    'name': 'collect_host',  # 任务名称
                    'setup': ''  # 执行模块
                }
            ]
        }

        play = Play().load(play_source, variable_manager=variable_manager, loader=loader)

        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory=inventory,
                variable_manager=variable_manager,
                loader=loader,
                options=options,
                passwords=passwords,
                stdout_callback=results_callback,
            )
            result = tqm.run(play)  # most interesting data for a play is actually sent to the callback's methods
        finally:
            if tqm is not None:
                tqm.cleanup()

            shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)