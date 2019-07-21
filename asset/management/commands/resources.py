# -*- coding: utf-8 -*-
# __author__="jiajun.zhu"
# DATE:2019/7/15

import shutil
import ansible.constants as C
import os
import json

from django.core.management import BaseCommand
from django.conf import settings

from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase

from asset.models import Hosts

class ResultCallback(CallbackBase):

    def __init__(self):
        super(ResultCallback, self).__init__()
        self._cache_host = {}

    def v2_runner_on_ok(self, result, **kwargs):
        self.actions = {
            'collect_host': self.collect_host,
            'copy_file': self.copy_file,
            'collect_resources': self.collect_resources,
        }
        func = self.actions.get(result.task_name)
        if func:
            func(result)
        # print(dir(result._host))
        # print(dir(result))
        # print(result)
        # print(result._host.name)
        # print(result.task_name)
        # print(result._result)

    def collect_host(self,result):
        # print(result)
        fact = result._result.get('ansible_facts',{})
        # 2.6.0 ansible版本中 ip获取是address，更高版本可能会变为network
        # ip = fact.get("ansible_default_ipv4").get("network",'')
        ip = fact.get("ansible_default_ipv4").get("address",'')
        self._cache_host[result._host.name] = ip

    def copy_file(self,result):
        pass

    def collect_resources(self,result):
        ip = self._cache_host.get(result._host.name)
        resources = result._result.get('stdout_lines',[])
        print(ip)
        print(resources)


class Command(BaseCommand):

    def handle(self,*args,**options):
        print('running task now......')
        Options = namedtuple('Options',
                             ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user', 'check',
                              'diff'])
        options = Options(connection='smart', module_path=[], forks=10, become=None, become_method=None,
                          become_user=None, check=False, diff=False)

        loader = DataLoader()  # Takes care of finding and reading yaml, json and ini files
        passwords = {}
        results_callback = ResultCallback()
        inventory = InventoryManager(loader=loader, sources=os.path.join(settings.BASE_DIR,"etc","hosts"))  # 剧本位置
        variable_manager = VariableManager(loader=loader, inventory=inventory)

        path_resource = '/tmp/resources.py'

        play_source = {
            'name': "test",
            'hosts': 'all',  # 在哪些主机上执行
            'gather_facts': 'no',
            'tasks': [  # 任务列表
                {
                    'name': 'collect_host',  # 任务名称
                    'setup': ''  # 执行模块
                },
                {
                    'name': 'copy_file',  # 任务名称
                    'copy': 'src={0} dest={1}'.format(os.path.join(settings.BASE_DIR,"etc","resources.py"),path_resource)  # 执行模块
                },
                {
                    'name': 'collect_resources',  # 任务名称
                    'command': 'python {0}'.format(path_resource)  # 执行模块
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