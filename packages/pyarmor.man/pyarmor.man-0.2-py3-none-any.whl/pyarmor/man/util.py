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
#  @File: pyarmor/man/util.py
#
#  @Author: Jondy Zhao(pyarmor@163.com)
#
#  @Create Date: Thu Jan  24 18:25:28 CST 2024
#
import logging

from urllib.request import urlopen
from urllib.error import HTTPError

logger = logging.getLogger('pyarmor.man')


def _get_remote_file(url, timeout=3.0):
    logger.debug('check url: %s', url)
    from ssl import _create_unverified_context as create_context
    return urlopen(url, timeout=timeout, context=create_context())


def check_server(url, timeout=3.0):
    """检查服务器数据，返回 HTTP 404，提示需要升级 pyarmor.man"""
    try:
        res = _get_remote_file(url, timeout=timeout)
        status = res.status
    except HTTPError as e:
        logger.debug('server error "%s"', str(e))
        status = e.status
    except Exception as e:
        logger.debug('network error "%s"', e)
        logging.warning(_('log_warn_1\n'))
        return

    logger.debug('server return %s', status)
    if status not in (200, 301, 302, 307, 308):
        logging.warning(
            _('log_warn_2\n') if status == 404 else
            _('log_warn_1\n')
        )
