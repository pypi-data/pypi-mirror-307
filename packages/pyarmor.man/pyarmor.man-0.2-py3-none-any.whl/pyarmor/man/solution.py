#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
#############################################################
#                                                           #
#      Copyright @ 2024 -  Dashingsoft corp.                #
#      All rights reserved.                                 #
#                                                           #
#      Pyarmor.Man                                          #
#                                                           #
#      Version: 1.0                                         #
#                                                           #
#############################################################
#
#
#  @File: pyarmor/man/solution.py
#
#  @Author: Jondy Zhao(pyarmor@163.com)
#
#  @Created: Wed Oct 23 18:51:52 CST 2024
#
"""常见问题的解决方案"""
import logging
import re

from collections import namedtuple

logger = logging.getLogger('pyarmor.man')

QueryItem = namedtuple(
    'QueryItem',
    'name, help, type, keys, value',
    defaults=('str', [], None)
)

ISSUE_DATA_ZH = (
    '在使用什么功能的时候出现了问题',
    [
        ('1', '注册 Pyarmor 许可证'),
        ('2', '生成加密脚本'),
        ('3', '运行加密脚本'),
        ('4', '安装 Pyarmor'),
    ],
)

FEATURE_DATA_ZH = (
    '你希望了解那一方面的内容',
    [
        ('安装和试用', None),
        ('许可模式和功能亮点', None),
        ('加密功能', None),
        ('发布加密脚本', None),
        ('设置加密脚本的有效期或者绑定加密脚本到固定设备', None),
        ('支持的平台和环境', None),
        ('定制和扩展', None),
    ]
)

LEARN_DATA_ZH = (
    '你打算如何学习',
    ['通过示例进行学习', '通过命令和选项进行学习']
)


MAN_DATA_ZH = (
    '需要 Pyarmor 助手为您做什么？',
    [
        ('1', '解决 Pyarmor 使用中遇到的问题'),
        ('2', '报告无法解决的问题'),
        ('3', '了解 Pyarmor 的功能'),
        ('4', '学习如何使用 Pyarmor')
    ],
)

MAN_DATA_EN = (
    'What can I do for you?',
    [
        ('1', 'Something is wrong with Pyarmor, find solutions'),
        ('2', 'Report issue can not be solved'),
        ('3', 'Understand Pyarmor features'),
        ('4', 'Learn how to use Pyarmor')
    ],
)


class UserAction:
    """用户执行 Pyarmor 动作基类

    每一步的动作都包括

      - 所在设备
      - 执行的命令和选项
      - 执行的结果
      - 目标设备（可选）

    """
    pass


class DeviceInfo:
    """收集用户设备信息"""

    DeviceForm = ('Physical Device: laptop, raspberry etc.',
                  'CI/CD Pipeline: GitHub action etc.',
                  'Local Docker Container',
                  'VM: Cloud Server, Qemu, Vbox etc.')

    OperationSystem = 'Linux', 'FreeBSD', 'Darwin', 'Windows'

    Arch = 'x86/64', 'arm', 'aarch64'

    def __init__(self, name):
        # 设备名称，仅用来标识和区别不同设备
        self.name = name

        # 是否联网
        self.online = None

        # 初始化设备信息
        self.init()

    def init(self):
        import platform
        self.system = platform.system()
        self.release = platform.release()
        self.platform = platform.platform()
        self.machine = platform.machine()
        self.python = platform.python_version_tuple()
        self.python_imp = platform.python_implementation()
        self.pyarmor = self.check_pyarmor()
        self.pyarmor_core = None

    def check_online(self, url=None):
        """通过连接到外部服务器判断是否能够联网"""
        from ssl import _create_unverified_context as context
        from urllib.request import urlopen
        from urllib.error import HTTPError

        url = 'https://pypi.org' if url is None else url
        logger.debug('check online by url: %s', url)
        try:
            res = urlopen(url, timeout=3.0, context=context())
            logger.debug('server return HTTP %d', res.status)
        except HTTPError as e:
            logger.debug('server return HTTP %d: %s', e.status, e)
        except Exception as e:
            logger.debug('network error "%s"', e)
            return False
        return True

    def check_pyarmor(self):
        try:
            from pyarmor.cli import __VERSION__ as ver
            return [x for x in ver.split('.')]
        except Exception as e:
            logger.debug('import pyarmor.cli error: %s', e)
            return False


class ManAction:
    """用户使用帮助系统进行交互动作的基类"""

    def __init__(self, cfg, arg):
        self.proxy = (
            RegisterSolution(cfg) if arg == 'register' else
            BuildSolution(cfg) if arg == 'build' else
            InstallSolution(cfg) if arg == 'install' else
            RuntimeSolution(cfg) if arg == 'runtime' else
            None
        )

    @property
    def prompt(self):
        """返回交互输入显示的提示符"""
        return self.proxy.prompt if self.proxy else ''

    @property
    def hint(self):
        """返回当前操作的帮助说明"""
        return self.proxy.hint if self.proxy else ''

    def handle(self, line=None):
        """交互处理用户的响应

        第一次开始处理的时候 line 为 None

        之后是用户输入的行，可能为空行

        返回 True 表示处理完成，否则继续接受用户的输入
        """
        return self.proxy.handle(line) if self.proxy else True


class Solution(ManAction):
    """解决问题的基类"""

    def __init__(self, cfg, arg=None):
        self.cfg = cfg
        self._prompt = 'solution prompt'
        self._hint = 'solution hint'
        self.device = DeviceInfo('local')
        self.query = None
        self.buginfo = {
            'error': QueryItem(
                'error',
                _('query_error_message\n'),
            )
        }

    @property
    def prompt(self):
        return self._prompt

    @property
    def hint(self):
        return self._hint

    def handle(self, answer=None):
        if answer is None:
            logger.debug('start to fix register issue')
            self.restart()
            return self.fix_issue()

        if self.query == 'EOF':
            if answer[:1].lower() in ('y', 'Y'):
                title, body = self.buginfo['error'].value
                self.report_issue(title, body)
            return True

        if self.query:
            item = self.buginfo[self.query]
            if item.keys:
                for x in item.keys:
                    if x.startswith(answer.lower()):
                        answer = x
                        break

                if answer in item.keys:
                    index = item.keys.index(answer)
                    item = item._replace(value=index)
                elif answer.isdigit():
                    index = int(answer) - 1
                    if index < len(item.keys):
                        item = item._replace(value=index)

            elif item.type == 'bool':
                value = answer.lower()[:1] in ('1', 'y', 't')
                item = item._replace(value=value)

            else:
                item = item._replace(value=answer)

            # 重新输入
            if item.value is None:
                return
            else:
                self.buginfo[self.query] = item

        return self.fix_issue()

    def show_solutions(self, solutions):
        if isinstance(solutions, str):
            solutions = [solutions]
        self._hint = '\n'.join(solutions + [''])
        self._prompt = _('solution_prompt')

    def query_item(self, name, hint=None):
        item = self.buginfo[name]
        prompt = {
            'str': _('query_string_prompt'),
            'bool': _('query_boolean_prompt'),
            'choice': _('query_selection_prompt'),
        }

        if item.value is None:
            self._prompt = prompt.get(item.type, '')
            self._hint = hint if hint else item.help
            self.query = name
        else:
            self._prompt = ''
            self._hint = ''
            self.query = None
            return item.value

    def clear_items(self, names):
        for name in names:
            old = self.buginfo.get(name, None)
            if old and old.value is not None:
                self.buginfo[name] = old._replace(value=None)

    def check_pyarmor_core(self, testrun=False):
        """通过加密一个简单的脚本，判断是否正确安装 pyarmor.cli.core"""
        from test.support import script_helper as helper, temp_cwd
        args = '-m', 'pyarmor.cli', 'gen', 'foo.py'
        kwargs = {
            '__isolated': False
        }

        logger.debug('checking pyarmor core ...')
        with temp_cwd():
            with open('foo.py', 'w') as f:
                f.write('print("Hello Pyarmor")')
            try:
                logger.debug('obfuscating simple script ...')
                res = helper.assert_python_ok(*args, **kwargs)
                logger.debug('obfuscating simple script END')
            except Exception as e:
                logger.debug('error: %s', e)
                return

            rc, stdout, stderr = res
            if rc == 0 and testrun:
                args = 'dist/foo.py',
                res = helper.assert_python_ok(*args, **kwargs)
                rc, stdout, stderr = res

            result = 'OK.' if rc == 0 else ('error: %s' % rc)
            logger.debug('checking pyarmor core %s', result)
            return rc == 0

    def check_log_file(self, logfile='pyarmor.bug.log'):
        logger.debug('check logfile %s', logfile)
        try:
            with open(logfile, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except Exception as e:
            logger.debug('logfile error: %s', e)

    def check_bug_log(self):
        errinfo = self.buginfo['error']
        if errinfo.value is None:
            logfile = 'pyarmor.bug.log'
            buglog = self.check_log_file(logfile)
            if not buglog:
                errinfo = errinfo._replace(value=False)
                self.buginfo['error'] = errinfo
                self.show_solutions(_('s_no_bug_log'))
                return
            if not buglog.startswith('[BUG]:'):
                errinfo = errinfo._replace(value=False)
                self.buginfo['error'] = errinfo
                self.show_solutions(_('s_invalid_bug_log'))
                return
            lines = buglog.splitlines()
            value = lines[0], '\n'.join(lines[1:])
            errinfo = errinfo._replace(value=value)
            self.buginfo['error'] = errinfo

    def append_man_log(self, body):
        logfile = 'pyarmor.man.log'
        with open(logfile, 'r', encoding='utf-8') as f:
            f.flush()
            manlog = f.read()
        title = '## Pyarmor Man Checklist'
        return '\n'.join([body, '', title, '```', manlog, '```'])

    def report_issue(self, title, body):
        """打开报告问题的网页

        根据模版生成一个临时文件，写入问题报告的标题和内容
        """
        from os import makedirs
        from os.path import join
        from html import escape

        page = WebPage(self.cfg, 'file report.html')
        src = page.url[len('file://'):]
        with open(src, 'r', encoding='utf-8') as f:
            data = f.read()

        dest = self.cfg['man']['data_path']
        makedirs(dest, exist_ok=True)
        dest = join(dest, 'report.html')

        with open(dest, 'w', encoding='utf-8') as f:
            f.write(data.replace(
                '{BugTitle}', escape(title)
            ).replace(
                '{BugBody}', escape(self.append_man_log(body))))
        page.handle('file://' + dest.replace('\\', '/'))

    def fix_issue(self):
        self.check_bug_log()

        errinfo = self.buginfo['error']
        if errinfo.value is False:
            self.show_solutions(_('s_no_bug_log'))
            return

        errmsg = errinfo.value[0][6:].strip()
        solutions = self.find_solutions(errmsg)
        if solutions:
            self.show_solutions(solutions)
            return

        self.query = 'EOF'
        self.show_solutions(
            _('s_no_solution').format(bug=errinfo.value[0])
        )
        self._prompt = _('s_no_solution_prompt')

    def find_solutions(self, errmsg):
        """根据错误信息设置相应的解决方案，返回字符串或者数组"""
        pass


class RegisterSolution(Solution):
    """解决注册 Pyarmor 的所有问题

    在注册失败的设备运行 Pyarmor Man 来解决注册问题

    通过和用户交互和自动检测，收集相关信息:

       许可证类型
       设备信息，操作系统，架构等
       Pyarmor 版本
       错误信息，从 .pyarmor/pyarmor.debug.log 中收集

    然后给出相应的解决方案，显示在网页中

    如果不能找到解决方案，生成问题报告，显示在网页中

    解决方案列表:

    1. 查看 v8.5.12 的 solutions 文档中注册失败解决方案
       适用于 pyarmor version < 9.0.4

    2. 尚未成功注册

       自动检查网络连接，自动检查 Python 是否可以访问网络
       是否请求太频繁（应该不会发生）
       自动检查错误日志，是否参数错误，是否产品名称不正确
       许可证的购买时间，是否有效

    3. 已经成功注册一次，在另外设备上注册失败

       自动检查网络连接，自动检查 Python 是否可以访问网络
       是否请求太频繁（应该不会发生）
       自动检查错误日志，是否参数错误，是否产品名称不正确

    4. 注册成功，pyarmor -v 能够看到注册信息，但是加密时候出错

    集团版许可证

    1. 设备的类型，是否 CI/CD，Docker container
    2. MachieID 是否发生变化
    3. 是否生成正确的设备注册文件
    4. 是否使用设备注册文件而不是设备文件进行注册
    """

    def __init__(self, cfg, arg=None):
        super().__init__(cfg, arg)
        self._prompt = '(man.issue.register) '
        self._hint = 'fix_register_issue'
        self.buginfo.update({
            'lictype': QueryItem(
                'lictype',
                _('query_license_type\n'),
                'choice',
                (
                    _('basic_license'),
                    _('pro_license'),
                    _('group_license'),
                    _('ci_license')
                ),
            ),

            'firstreg': QueryItem(
                'firstreg',
                _('query_is_firstreg\n'),
                'bool',
            ),

            'offdev': QueryItem(
                'offdev',
                _('query_is_offline_device\n'),
                'bool',
            ),
        })

    def restart(self):
        """清空用户选择的选项"""
        self.clear_items(['lictype', 'error'])

    def fix_issue(self):
        """开始处理问题，收集必要的信息"""
        device = self.device
        if device.pyarmor is False:
            self.show_solutions(_('s_install_pyarmor'))
            return

        if int(device.pyarmor[0]) < 9:
            self.show_solutions(_('s_upgrade_pyarmor'))
            return

        lictype = self.query_item('lictype')
        if lictype is None:
            return

        # firstreg = self.query_item('firstreg')
        # if firstreg is None:
        #     return

        if lictype in (0, 1):
            if device.online is None:
                device.online = device.check_online()

            if not device.online:
                self.show_solutions(_('s_need_internet'))
                return

            if device.pyarmor_core is None:
                device.pyarmor_core = self.check_pyarmor_core()

            if not device.pyarmor_core:
                self.show_solutions(_('s_install_pyarmor_core'))
                return

        elif lictype == 2:
            if device.pyarmor_core is None:
                device.pyarmor_core = self.check_pyarmor_core()

            if not device.pyarmor_core:
                self.show_solutions(_('s_install_pyarmor_core'))
                return

            offdev = self.query_item('offdev')
            if offdev is None:
                return

            if not offdev:
                if device.online is None:
                    device.online = device.check_online()

                if not device.online:
                    self.show_solutions(_('s_need_internet'))
                    return

        elif lictype == 3:
            pass

        return super().fix_issue()


class InstallSolution(Solution):

    def __init__(self, cfg, arg=None):
        super().__init__(cfg, arg)
        self._prompt = '(man.issue.install) '
        self._hint = 'fix_install_issue'

    def find_solutions(self, errmsg):
        """根据错误信息设置相应的解决方案"""
        pass

    def restart(self):
        """清空用户选择的选项"""
        pass

    def fix_issue(self):
        """开始处理问题，收集必要的信息"""
        pass


class BuildSolution(Solution):

    def __init__(self, cfg, arg=None):
        super().__init__(cfg, arg)
        self._prompt = '(man.issue.build) '
        self._hint = 'fix_build_issue'
        self.buginfo.update({
            'fewest': QueryItem(
                'fewest',
                _('query_is_fewest_option\n'),
                'bool',
            ),
        })

    def restart(self):
        """清空用户选择的选项"""
        self.clear_items(['fewest', 'error'])

    def fix_issue(self):
        """开始处理问题，收集必要的信息"""
        device = self.device
        if device.pyarmor is False:
            self.show_solutions(_('s_install_pyarmor'))
            return

        if int(device.pyarmor[0]) < 9:
            self.show_solutions(_('s_upgrade_pyarmor'))
            return

        if device.pyarmor_core is None:
            device.pyarmor_core = self.check_pyarmor_core()

        if not device.pyarmor_core:
            self.show_solutions(_('s_install_pyarmor_core'))
            return

        self.check_bug_log()
        if self.buginfo['error'].value is False:
            self.show_solutions(_('s_no_bug_log'))
            return

        # 试用版和集团版许可证不需要联网
        body = self.buginfo['error'].value[1]
        if all([body.find('(%s), ' % x) == -1 for x in ('group', 'trial')]):
            if device.online is None:
                device.online = device.check_online()

            if not device.online:
                self.show_solutions(_('s_need_internet'))
                return

        fewest = self.query_item('fewest')
        if fewest is None:
            return

        if not fewest:
            for name in ('error', 'fewest'):
                old = self.buginfo[name]
                self.buginfo[name] = old._replace(value=None)
            return

        return super().fix_issue()


class RuntimeSolution(Solution):

    def __init__(self, cfg, arg=None):
        super().__init__(cfg, arg)
        self._prompt = '(man.issue.runtime) '
        self._hint = 'fix_runtime_issue'
        self.target = DeviceInfo('target')
        self.buginfo.update({
            'error': QueryItem(
                'error',
                _('query_runtime_log\n'),
            ),
            'fewest': QueryItem(
                'fewest',
                _('query_is_fewest_option\n'),
                'bool',
            ),
            'no_cross': QueryItem(
                'no_cross',
                _('query_is_same_platform\n'),
                'bool',
            ),
            'simple_cross': QueryItem(
                'simple_cross',
                _('query_simple_cross\n'),
                'bool',
            ),
            'local_cross': QueryItem(
                'local_cross',
                _('query_local_cross\n'),
                'bool',
            ),
            'simple': QueryItem(
                'simple',
                _('query_run_simple_script\n'),
                'bool',
            ),
            'advice': QueryItem(
                'advice',
                'show advice',
                'bool',
            ),
            'pack': QueryItem(
                'pack',
                'query_is_pack',
                'bool',
            ),
            'pack_plain': QueryItem(
                'pack',
                _('query_pack_plain\n'),
                'bool',
            ),
            'pack_simple': QueryItem(
                'pack',
                _('query_pack_simple\n'),
                'bool',
            ),
            'prior_pack': QueryItem(
                'pack',
                _('query_prior_pack\n'),
                'bool',
            ),
            'dbglog': QueryItem(
                'dbglog',
                _('query_debug_log\n'),
                'str',
            )
        })

    def restart(self):
        """清空用户选择的选项"""
        self.clear_items([
            'fewest', 'cross', 'simple', 'dbglog', 'error', 'advice',
            'pack', 'pack_plain', 'pack_simple', 'prior_pack'
        ])

    def report_runtime_issue(self, pack=False):
        runlog = self.check_runtime_log()
        if runlog is None:
            return

        title = '[BUG][Runtime] %s' % runlog[0]
        body = ['## Runtime logs', '```'] + runlog[1:] + ['```']

        lines = self.buginfo['dbglog'].value.splitlines()
        n = len(lines)
        if n < 50:
            buildlog = [self.buginfo['dbglog'].value]
        else:
            buildlog = lines[:30] + ['', '...', ''] + lines[-10:]
        body.extend(['', '## Build logs', '```'] + buildlog + ['```'])

        self.report_issue(title, '\n'.join(body))
        self._hint = ''
        self._prompt = _('solution_prompt')

    def report_cross_issue(self):
        return self.report_runtime_issue()

    def report_pack_issue(self):
        return self.report_runtime_issue()

    def try_solution(self, solution, pack=False):
        """提示用户可能的解决方案，如果不能解决问题，就报告问题"""
        advice = self.query_item('advice', hint=solution)
        if advice is None:
            return
        if not advice:
            return self.report_runtime_issue(pack=pack)

    def check_debug_log(self):
        logfile = 'pyarmor.debug.log'
        log = self.check_log_file(logfile)
        if not log:
            return

        item = self.buginfo['dbglog']
        self.buginfo['dbglog'] = item._replace(value=log)

        mark = ' args: ['
        n = log.find(mark)
        if n == -1:
            logger.debug('no found args in debug log')
            return

        k = log.find(']', n)
        try:
            args = eval(log[n+len(mark)-1:k+1])
        except Exception:
            args = log[n+len(mark)-1:k+1]
            logger.debug('invalid args: %s', args)
            return

        return args

    def check_runtime_log(self, logfile='run.log'):
        """读取执行脚本的错误日志，返回错误信息行和控制台输出"""
        error = self.query_item('error')
        if error is None:
            return
        if 'crashed'.startswith(error.lower()):
            return ['[Crashed]', '']
        if error.lower() in ('y', 'yes'):
            log = self.check_log_file(logfile)
            if log:
                lines = log.splitlines()
                pat = re.compile(r'^[a-zA-Z]*(Error|Exception): .*$')
                for line in reversed(lines):
                    if pat.match(line):
                        title = line
                        break
                else:
                    title = lines[-1]
                return [title] + lines

    def fix_issue(self):
        """开始处理问题，收集必要的信息"""
        cmd_opts = self.check_debug_log()
        if not cmd_opts:
            self.show_solutions(_('s_need_debug_log'))
            return

        # 跨平台发布
        no_cross = self.query_item('no_cross')
        if no_cross is None:
            return

        if not no_cross:
            simple_cross = self.query_item('simple_cross')
            if simple_cross is None:
                return
            if not simple_cross:
                self.try_solution(_('s_runtime_simple_cross'))
                return

            local_cross = self.query_item('local_cross')
            if local_cross is None:
                return
            if not local_cross:
                item = self.buginfo['cross']
                self.buginfo['cross'] = item._replace(value=False)
            else:
                self.report_runtime_issue()
                return

        # 打包加密脚本
        if '--pack' in cmd_opts:
            pack_plain = self.query_item('pack_plain')
            if pack_plain is None:
                return
            if not pack_plain:
                self.show_solutions(_('s_runtime_pack_plain'))
                return

            prior_pack = self.query_item('prior_pack')
            if prior_pack is None:
                return
            if not prior_pack:
                item = self.buginfo['pack']
                self.buginfo['pack'] = item._replace(value=False)
            else:
                pack_simple = self.query_item('pack_simple')
                if pack_simple is None:
                    return
                if not pack_simple:
                    self.report_runtime_issue(pack=True)
                    return

                fewest = self.query_item('fewest')
                if fewest is None:
                    return

                self.try_solution(_('s_runtime_pack'), pack=True)
                return

        if '--enable-bcc' in cmd_opts:
            simple = self.query_item('simple')
            if simple is None:
                return
            if not simple:
                self.report_runtime_issue()
                return
            self.try_solution(_('s_runtime_bcc'))
            return

        if '--enable-rft' in cmd_opts:
            simple = self.query_item('simple')
            if simple is None:
                return
            if not simple:
                self.report_runtime_issue()
                return
            self.try_solution(_('s_runtime_rft'))
            return

        restrict_opts = (
            '--private', '--restrict',
            '--assert-call', '--assert-import'
        )
        if any([x in cmd_opts for x in restrict_opts]):
            simple = self.query_item('simple')
            if simple is None:
                return
            if not simple:
                self.report_runtime_issue()
                return
            self.try_solution(_('s_runtime_restrict'))
            return

        return self.report_runtime_issue()


class WebPage(ManAction):
    """打开指定网页"""

    def __init__(self, cfg, arg):
        proto, path = arg.split()
        cfg = cfg['man']
        lang = cfg['runtime.lang']
        parts = []
        if proto == 'file':
            pre = 'file://' + cfg['base_path'].replace('\\', '/')
            parts = (pre, 'assets', lang, path)
        else:
            parts = cfg['docurl'].format(lang=lang), path
        self.url = '/'.join(parts)

    def handle(self, url=None):
        import webbrowser
        url = self.url if url is None else url
        logger.debug('open file: %s', url)
        if not webbrowser.open(url):
            logger.error('can not open file: %s', url)
        return True
