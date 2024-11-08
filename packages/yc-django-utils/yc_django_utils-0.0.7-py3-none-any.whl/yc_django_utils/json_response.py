"""
Created on 2024-02-26
@author:刘飞
@description: 自定义的JsonResponse文件
"""
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status


class SuccessResponse(Response):
    """
    标准响应成功的返回, SuccessResponse(data)或者SuccessResponse(data=data)
    (1)默认code返回200, 不支持指定其他返回码
    """

    def __init__(self, data=None, msg='success', status=None, template_name=None, headers=None, exception=False,
                 content_type=None, page=1, limit=1, total=1):
        std_data = {
            "code": 200,
            "page": page,
            "limit": limit,
            "total": total,
            "data": data,
            "msg": msg
        }
        super().__init__(std_data, status, template_name, headers, exception, content_type)


class DetailResponse(Response):
    """
    不包含分页信息的接口返回,主要用于单条数据查询
    (1)默认code返回200, 不支持指定其他返回码
    """

    def __init__(self, data=None, msg='success', status=None, template_name=None, headers=None, exception=False,
                 content_type=None, ):
        std_data = {
            "code": 200,
            "data": data,
            "msg": msg
        }
        super().__init__(std_data, status, template_name, headers, exception, content_type)


class ErrorResponse(Response):
    """
    标准响应错误的返回,ErrorResponse(msg='xxx')
    (1)默认错误码返回400, 也可以指定其他返回码:ErrorResponse(code=xxx)
    """

    def __init__(self, data=None, msg='error', code=400, status=None, template_name=None, headers=None,
                 exception=False, content_type=None):
        std_data = {
            "code": code,
            "data": data,
            "msg": msg
        }
        super().__init__(std_data, status, template_name, headers, exception, content_type)


# 自定义错误页面时返回
def bad_request(request, exception):
    data = {'code': status.HTTP_400_BAD_REQUEST, 'msg': '参数错误', 'data': None}
    return JsonResponse(data=data, status=status.HTTP_400_BAD_REQUEST)


def permission_denied(request, exception):
    data = {'code': status.HTTP_403_FORBIDDEN, 'msg': '无权限', 'data': None}
    return JsonResponse(data=data, status=status.HTTP_403_FORBIDDEN)


def page_not_found(request, exception):
    data = {'code': status.HTTP_404_NOT_FOUND, 'msg': '资源不存在', 'data': None}
    return JsonResponse(data=data, status=status.HTTP_404_NOT_FOUND)


def page_error(exception):
    data = {'code': status.HTTP_500_INTERNAL_SERVER_ERROR, 'msg': '服务器错误', 'data': None}
    return JsonResponse(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
