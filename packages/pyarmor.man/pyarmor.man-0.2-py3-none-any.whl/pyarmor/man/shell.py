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
#  @File: pyarmor/man/shell.py
#
#  @Author: Jondy Zhao (pyarmor@163.com)
#
#  @Create Date: Sat Jul 20 06:06:03 CST 2024
#

"""Pyarmor 交互帮助系统

实现命令 `pyarmor-man`，通过命令行方式帮助用户快速解决使用过程中遇到
的问题，学习使用 Pyarmor，以及报告存在的问题

通用使用说明
------------

- 直接回车显示使用帮助
- TAB 根据上下文自动补齐输入内容
- 在用户进行选择的时候，使用 TAB 可以循环进行切换
- Ctrl+D 返回上一层，如果在最顶层那么退出帮助系统

注意
----

在 MacOS 下面，使用 TAB 自动补齐功能需要额外配置

示例
----

进入交互模式::

    $ pyarmor-man

或者直接进入解决问题模式::

    $ pyarmor-man issue

"""

import argparse
import cmd
import configparser
import gettext
import logging
import logging.config
import os
import sys

from . import __version__
from .util import logger, check_server
from .navigate import Navigator
from .solution import ManAction


BASE_PATH = os.path.dirname(__file__)
CONFIG_FILE = os.path.join(BASE_PATH, 'default.cfg')
USER_HOME = os.path.expanduser('~')
DATA_PATH = os.path.join(USER_HOME, '.pyarmor', 'man')


class ManShell(cmd.Cmd):

    intro = 'Welcome to Pyarmor Man'
    prompt = '(man) '

    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx
        self.nav = Navigator(self.ctx)
        self.intro = _('shell_welcome\n')
        self.prompt = _('shell_prompt')
        self.step = 0

    def emptyline(self):
        self.do_help()

    def default(self, line, complete=False):
        """Got user response interactively"""
        if line == 'EOF':
            self.columnize([''])
            if isinstance(self.nav.pop(), ManAction):
                self.nav.pop()
            if self.nav.path:
                self.prompt = self.nav.prompt
                self.do_help()
            else:
                return True

        elif isinstance(self.nav.top, ManAction):
            if self.nav.top.handle(line):
                return self.default('EOF')
            self.prompt = self.nav.prompt
            self.do_help()

        else:
            navitem = self.nav.top
            cmd, *rest = line.split(maxsplit=1)

            if cmd not in navitem.keys:
                for key in navitem.keys:
                    if key.startswith(cmd):
                        cmd = key
                        break

            if cmd in navitem.keys:
                navitem = self.nav.push(cmd)
                self.prompt = self.nav.prompt
                if rest:
                    return self.default(rest[0])
                if navitem.keys:
                    self.do_help()
                elif navitem.children:
                    child = navitem.children[0]
                    if child.handle():
                        self.nav.pop()
                    else:
                        self.nav.push(child)
                    self.do_help()
                    self.prompt = self.nav.prompt

            else:
                hint = _('unknown_cmd').format(cmd=cmd)
                self.columnize([self.step_hint()])
                self.columnize([hint])
                self.do_help()

    def completedefault(self, text, line, begidx, endidx):
        return self.nav.complete(text, line, begidx, endidx)

    def step_hint(self):
        self.step += 1
        return '\n'.join(['', '*' * 60, '* %s' % self.step, '*'])

    def do_help(self, arg=None):
        self.columnize([self.step_hint()])
        self.columnize([self.nav.hint])

    def do_quit(self, args=None):
        return True


def select_language(cfg):
    lang = cfg['man'].get('lang', 'auto')
    if lang == 'auto':
        lang = os.getenv('LANG', 'en_US')
    logger.debug('select language "%s"', lang)
    lang = cfg['man']['runtime.lang'] = lang.split('_', 1)[0]
    lang = 'zh_CN' if lang == 'zh' else 'en_US'
    path = os.path.join(os.path.dirname(__file__), 'locale')
    gettext.translation(
        'pyarmor', localedir=path, languages=[lang]
    ).install()


def main_parser():
    parser = argparse.ArgumentParser(
        prog='pyarmor-man',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument('-v', '--version', action='version',
                        version=__version__)
    parser.add_argument('-e', '--encoding', help=_('opt_encoding'))
    parser.add_argument('-c', '--cached', action='store_true',
                        help=_('opt_cached'))
    parser.add_argument('cmd', nargs='?')

    return parser


def main():
    logging.config.fileConfig(CONFIG_FILE)

    cfg = configparser.ConfigParser(
        empty_lines_in_values=False,
        interpolation=configparser.ExtendedInterpolation(),
    )
    cfg.read([CONFIG_FILE], encoding='utf-8')
    cfg['man']['base_path'] = BASE_PATH
    cfg['man']['data_path'] = DATA_PATH

    select_language(cfg)

    parser = main_parser()
    args = parser.parse_args(sys.argv[1:])
    logger.debug('args: %s', args)
    logger.debug('data path: %s', DATA_PATH)

    if not args.cached:
        checkurl = cfg.get('man', 'checkurl')
        timeout = cfg['man'].getint('timeout', 3.0)
        check_server(checkurl, timeout=timeout)

    try:
        ManShell(cfg).cmdloop()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        from traceback import format_exc
        logger.debug('unexpected exception\n%s', format_exc())
        logger.error('%s', str(e))


if __name__ == '__main__':
    main()
