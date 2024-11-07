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
#  @File: pyarmor/man/report.py
#
#  @Author: Jondy Zhao(pyarmor@163.com)
#
#  @Created: Wed Oct 23 07:42:52 CST 2024
#
"""提交 Pyarmor Man 无法解决的问题报告

支持的提交方式

- 直接提交到 GitHub Pyarmor 的问题列表
- 发送邮件到 pyarmor@163.com ，仅用于不适合公开的问题

如果当前环境有 `gh` 命令，并且已经登陆，那么直接调用 gh 提交问题

否则打开一个网页，显示问题的标题和重现步骤

让用户选择发送邮件还是人工直接提交到 GitHub

GitHub REST API 参考
--------------------

提交新的报告到 `Pyarmor 错误表`__::

  curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/issues \
  -d '{"title":"Found a bug","body":"I'\''m having a problem with this.","assignees":["octocat"],"milestone":1,"labels":["bug"]}'

  Response: Status 201
  {
    "id": 1,
    "node_id": "MDU6SXNzdWUx",
    "url": "https://api.github.com/repos/octocat/Hello-World/issues/1347",
    ...
    "html_url": "https://github.com/octocat/Hello-World/issues/1347",
    "number": 1347,
    "state": "open",
    "title": "Found a bug",
    "body": "I'm having a problem with this.",
    "user": {
      "login": "octocat",
      ...
    },
  }

查看提交的错误报告::

  curl -L \
    -H "Accept: application/vnd.github+json" \
    -H "Authorization: Bearer <YOUR-TOKEN>" \
    -H "X-GitHub-Api-Version: 2022-11-28" \
    https://api.github.com/repos/OWNER/REPO/issues/ISSUE_NUMBER

  curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/issues/ISSUE_NUMBER/comments

  Response: status 200

  [
    {
      "id": 1,
      "node_id": "MDEyOklzc3VlQ29tbWVudDE=",
      "url": "https://api.github.com/repos/octocat/Hello-World/issues/comments/1",
      "html_url": "https://github.com/octocat/Hello-World/issues/1347#issuecomment-1",
      "body": "Me too",
      "user": {
        "login": "octocat",
        ...
      },
      "created_at": "2011-04-14T16:00:49Z",
      "updated_at": "2011-04-14T16:00:49Z",
      "issue_url": "https://api.github.com/repos/octocat/Hello-World/issues/1347",
      "author_association": "COLLABORATOR"
    }
  ]

添加注释到错误报告::

  curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/issues/ISSUE_NUMBER/comments \
  -d '{"body":"Me too"}'

  Response: status 201

  {
    "id": 1,
    "node_id": "MDEyOklzc3VlQ29tbWVudDE=",
    "url": "https://api.github.com/repos/octocat/Hello-World/issues/comments/1",
    "html_url": "https://github.com/octocat/Hello-World/issues/1347#issuecomment-1",
    ...
  }

查看，修改和删除单个注释::

  /repos/{owner}/{repo}/issues/comments/{comment_id}

  curl -L \
    -H "Accept: application/vnd.github+json" \
    -H "Authorization: Bearer <YOUR-TOKEN>" \
    -H "X-GitHub-Api-Version: 2022-11-28" \
    https://api.github.com/repos/OWNER/REPO/issues/comments/COMMENT_ID

  Response: status 200, comment data

  curl -L \
    -X PATCH \
    -H "Accept: application/vnd.github+json" \
    -H "Authorization: Bearer <YOUR-TOKEN>" \
    -H "X-GitHub-Api-Version: 2022-11-28" \
    https://api.github.com/repos/OWNER/REPO/issues/comments/COMMENT_ID \
    -d '{"body":"Me too"}'

  Response: status 200, comment data

  curl -L \
    -X DELETE \
    -H "Accept: application/vnd.github+json" \
    -H "Authorization: Bearer <YOUR-TOKEN>" \
    -H "X-GitHub-Api-Version: 2022-11-28" \
    https://api.github.com/repos/OWNER/REPO/issues/comments/COMMENT_ID

    Response: status 204, no data

把用户提问提交到 `Pyarmor 讨论区`__ （暂未实现）

在 Windows 下面需要安装 curl，Linux 和 MacOS 一般都自带

curl for Windows: https://curl.se/windows/

. _Pyarmor 错误表:
   https://github.com/dashingsoft.com/pyarmor/issues

. _Pyarmor 讨论区:
   https://github.com/dashingsoft/pyarmor/discussions/

"""
import logging

from subprocess import check_output


logger = logging.getLogger('pyarmor.man')


def send_request(url, timeout=3.0):
    logger.debug('check url: %s', url)
    check_output(['curl', url])
