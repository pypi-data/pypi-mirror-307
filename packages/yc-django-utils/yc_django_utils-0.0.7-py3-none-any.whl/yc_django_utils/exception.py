"""
Created on 2024-07-02
@author:刘飞
@description: 自定义异常处理
"""
import logging
import traceback

from django.db.models import ProtectedError
from django.http import Http404
from rest_framework.exceptions import APIException as DRFAPIException, AuthenticationFailed
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.views import set_rollback, exception_handler

from .json_response import ErrorResponse

logger = logging.getLogger(__name__)


def custom_exception_handler(ex, context):
    """
    统一异常拦截处理
    目的:(1)取消所有的500异常响应,统一响应为标准错误返回
        (2)准确显示错误信息
    :param ex:
    :param context:
    :return:
    """
    # print(f"ex->{ex}, context->{context}")
    msg = ''
    code = 400
    # 调用默认的异常处理函数
    response = exception_handler(ex, context)
    # 先对ex类型作判断处理
    if isinstance(ex, AuthenticationFailed) or isinstance(ex, InvalidToken):  # 用户认证失败
        # 如果是身份验证错误
        if response and response.data.get('detail') == "Given token not valid for any token type":
            code = 401
            msg = ex.detail
        elif response and response.data.get('detail') == "Token is blacklisted":
            # token在黑名单
            return ErrorResponse(status=HTTP_401_UNAUTHORIZED)
        else:
            code = 401
            msg = "Token is invalid or expired"
    elif isinstance(ex, Http404):
        code = 404
        msg = "接口地址不正确"
    elif isinstance(ex, DRFAPIException):
        set_rollback()
        msg = ex.detail
        if isinstance(msg, dict):
            for k, v in msg.items():
                for i in v:
                    msg = "%s:%s" % (k, i)
    elif isinstance(ex, ProtectedError):
        set_rollback()
        msg = "删除失败:该条数据与其他数据有相关绑定"
    elif isinstance(ex, Exception):
        logger.exception(traceback.format_exc())
        msg = str(ex)

    # 对response细节做判断
    if response is not None:
        if isinstance(response.data, list):  # 列表处理成字符串
            msg = response.data[0]
        elif isinstance(response.data, dict):  # 字典处理成字符串
            _msg = ''
            for _k, _v in zip(response.data.keys(), response.data.values()):
                _msg += f"{_k}: {_v[0] if isinstance(_v, list) else _v}"
            msg = _msg
    return ErrorResponse(msg=msg, code=code)
