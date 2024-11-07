#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
#############################################################
#                                                           #
#      Copyright @ 2023 -  Dashingsoft corp.                #
#      All rights reserved.                                 #
#                                                           #
#      Pyarmor Man                                          #
#                                                           #
#      Version: 1.0                                         #
#                                                           #
#############################################################
#
#
#  @File: pyarmor/man/navigate.py
#
#  @Author: Jondy Zhao (pyarmor@163.com)
#
#  @Create Date: Wed Oct 23 10:18:37 CST 2024
#

"""Pyarmor 帮助系统的导航条目"""
from collections import namedtuple

from .solution import ManAction, WebPage


NavItem = namedtuple(
    'NavItem',
    'name, title, hint, keys, children'
)


class Navigator(object):
    """导航用户，进入相关功能模块

    可用的功能模块

    - 下一级导航
    - 打开网页
    - 输入对象，包含所有的属性
    - 报告问题
    - 解决问题

    """

    def __init__(self, cfg):
        self.cfg = cfg
        root = self.load()
        self.path = [root]

    @property
    def top(self):
        return self.path[-1]

    @property
    def prompt(self):
        item = self.top
        return (item.prompt if isinstance(item, ManAction) else
                item.title)

    @property
    def hint(self):
        return self.top.hint

    def push(self, obj):
        if isinstance(obj, ManAction):
            self.path.append(obj)
        elif obj in self.top.keys:
            item = self.top.children[self.top.keys.index(obj)]
            self.path.append(item)
            return item

    def pop(self):
        return self.path.pop()

    def complete(self, text, line, begidx, endidx):
        pass

    def load(self, lang='en'):
        data = {
            'issue': (
                'issue',
                _('shell_prompt'),
                _('cmd_issue_help\n'),
                ('register', 'build', 'runtime'),
                [('register',
                  'register_issue_title',
                  '',
                  [], ['solution register']
                  ),
                 ('build',
                  'build_issue_title',
                  '',
                  [], ['solution build']
                  ),
                 ('runtime',
                  'runtime_issue_title',
                  '',
                  [], ['solution runtime']
                  )],
            ),

            'learn': (
                'learn',
                _('shell_prompt'),
                _('cmd_learn_help\n'),
                ('feature', 'command', 'example'),
                [('feature',
                  'learn_feature_title',
                  'file assets/learn/features.html',
                  [], ['docurl #table-of-contents']
                  ),
                 ('command',
                  'learn_command_title',
                  'file assets/learn/commands.html',
                  [], ['docurl reference/man.html']
                  ),
                 ('example',
                  'learn_example_title',
                  'file assets/examples/index.html',
                  [], ['docurl part-2.html']
                  )],
            ),
        }

        root = (
            'man',
            _('shell_prompt'),
            _('cmd_man_help\n'),
            ('issue', 'learn'),
            [data['issue'], data['learn']]
        )

        def mkitem(data):
            if isinstance(data, str):
                name, arg = data.split()
                if name in ('docurl', 'file'):
                    return WebPage(self.cfg, data)
                elif name == 'solution':
                    return ManAction(self.cfg, arg)

            assert isinstance(data, tuple)
            item = NavItem(*data)
            item.children[:] = [mkitem(x) for x in item.children]
            return item

        return mkitem(root)
