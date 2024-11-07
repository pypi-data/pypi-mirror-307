==============
 Pyarmor 助手
==============

Pyarmor 助手用来帮助学习 Pyarmor，快速解决使用过程中的问题，以及使用标准模版提交问题报告

安装
====

Pyarmor 助手可以直接使用 pip 进行安装。例如::

    $ python -m pip install pyarmor.man

开始
====

直接执行命令 `pyarmor-man` 进入助手模式::

    $ pyarmor-man

    欢迎使用 Pyarmor 帮助系统。 直接回车显示所有选项

    输入选项名称或者首字母并回车进入相应上下文

    Tab        补全选项
    Ctrl+D     返回上级
    Ctrl+C     退出帮助

    需要 Pyarmor 助手为您做什么？

    issue      解决 Pyarmor 使用中遇到的问题
    learn      了解和学习如何使用 Pyarmor

    请输入选项名称:

学习 Pyarmor
============

输入 ``learn`` 然后按下 :kbd:`Enter`::

    请输入选项名称: learn

然后选择学习方式::

    选择学习 Pyarmor 的方式

      example    通过例子来学习
      command    学习命令和选项
      feature    浏览所有的功能

      Ctrl+D     返回

    请输入选项名称:

输入 :kbd:`c` 并 :kbd:`Enter` 在网页打开命令手册::

    Please type command: c

输入 :kbd:`Ctrl+D` 离开学习环境，返回助手环境::

    需要 Pyarmor 助手为您做什么

      issue  解决 Pyarmor 使用中遇到的问题
      learn  了解和学习如何使用 Pyarmor

      Ctrl+D 退出

    请输入选项名称:

解决问题
========

Pyarmor 助手能够解决大部分使用过程中问题

输入 :kbd:`i` 或者 ``issue`` 然后按下 :kbd:`Enter` ，进入解决问题模式::

    请输入选项名称:  i

    问题发生在

      register    注册 Pyarmor 的时候
      build       生成加密脚本的时候
      runtime     运行加密脚本的时候

      Ctrl+D      返回

    请输入选项名称:

按照助手的提示来解决问题。例如，输入 :kbd:`reg` 来解决注册问题::

    请输入选项名称:  reg

    所使用的许可证类型

    1. 基础版
    2. 专家版
    3. 集团版
    4. 管线版

    请输入序号或者选项:

.. note::

   对于运行加密脚本的问题，请在构建设备上运行 Pyarmor 助手来解决问题

报告问题
--------

如果 Pyarmor 助手不能解决问题，会有如下提示::

    No found solution for this error:

    Would you like to report this issue to Pyarmor?

    Please type Y or N:

输入 :kbd:`y` 会打开报告问题的网页，其中标题和正文已经被 Pyarmor 助手自动生成

请对正文进行必要的补充说明，然后选择任意一种方式提交问题报告

- 点击按钮 `发送邮件` 到 Pyarmor 开发组
- 点击按钮 `提交到 GitHub`__

__ https://github.com/dashingsoft.com/pyarmor/issues
