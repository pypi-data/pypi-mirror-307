"""
Created on 2024-08-23
@author:LiuFei
@description
# 初始化基类【初始化数据使用 django 的 fixtures】
"""
import json
import os
import logging
from django.apps import apps
from django.db import transaction
from rest_framework import request
from django.contrib.auth import get_user_model
from django.conf import settings

logger = logging.getLogger(__name__)
Users = get_user_model()


class CoreInitialize:
    """
    使用方法：继承此类，重写 run方法，在 run 中调用 save 进行数据初始化
    """
    creator_id = None
    reset = False
    request = request
    file_path = None

    def __init__(self, reset=False, creator_id=None, app=None):
        """
        reset: 是否重置初始化数据
        creator_id: 创建人id
        app: 执行数据初始化的app
        """
        self.reset = reset or self.reset
        self.creator_id = creator_id or self.creator_id
        self.app = app or ''
        self.request.user = Users.objects.order_by('create_time').first()

    @transaction.atomic  # 添加事务
    def init_base(self, Serializer, unique_fields=None):
        """
        serializer:模型的序列化
        unique_fields:唯一性限制
        """
        model = Serializer.Meta.model
        # 根据路径找到初始化文件【例如apps.users 下的MyUser模型，则路径为apps/users/fixtures/init_myuser.json】
        path_file = os.path.join(apps.get_app_config(self.app.split('.')[-1]).path, 'fixtures',
                                 f'init_{Serializer.Meta.model._meta.model_name}.json')
        if not os.path.isfile(path_file):
            logger.info(f"文件不存在，跳过初始化:{path_file}")
            return
        with open(path_file, encoding="utf-8") as f:
            for data in json.load(f):
                filter_data = {}
                # 配置过滤条件,如果有唯一标识字段则使用唯一标识字段，否则使用全部字段[重点-查找后会更新指定条目,没有则创建]
                if unique_fields:
                    for field in unique_fields:
                        if field in data:
                            filter_data[field] = data[field]
                else:
                    for key, value in data.items():
                        # 列表和空单独处理
                        if isinstance(value, list) or not value:
                            continue
                        filter_data[key] = value
                instance = model.objects.filter(**filter_data).first()
                data["reset"] = self.reset
                serializer = Serializer(instance, data=data, request=self.request)
                serializer.is_valid(raise_exception=True)
                serializer.save()
        logger.info(f"[{self.app}][{model._meta.model_name}]初始化完成")

    def save(self, obj, data: list, name=None, no_reset=False):
        """

        """
        name = name or obj._meta.verbose_name
        logger.info(f"正在初始化[{obj._meta.label} => {name}]")
        if not no_reset and self.reset and obj not in settings.INITIALIZE_RESET_LIST:  # 重置则删除所有
            try:
                obj.objects.all().delete()
                settings.INITIALIZE_RESET_LIST.append(obj)
            except Exception:
                pass
        for ele in data:
            m2m_dict = {}
            new_data = {}
            for key, value in ele.items():
                # 判断传的 value 为 list 的多对多进行抽离，使用set 进行更新
                if isinstance(value, list) and value and isinstance(value[0], int):
                    m2m_dict[key] = value
                else:
                    new_data[key] = value
            _object, _ = obj.objects.get_or_create(id=ele.get("id"), defaults=new_data)
            # 多对多处理
            for key, m2m in m2m_dict.items():
                m2m = list(set(m2m))
                if m2m and len(m2m) > 0 and m2m[0]:
                    if _object.key:
                        value_list = _object.key.all().values_list('id', flat=True)
                        value_list = list(set(list(value_list) + m2m))
                        _object.key.set(value_list)
        #                     exec(f"""
        # if object.{key}:
        #     values_list = object.{key}.all().values_list('id', flat=True)
        #     values_list = list(set(list(values_list) + {m2m}))
        #     object.{key}.set(values_list)
        # """)
        logger.info(f"初始化完成[{obj._meta.label} => {name}]")

    @transaction.atomic  # 添加事务
    def init_treebeard(self, model, unique_fields=None, *args, **kwargs):
        """
        初始化树形结构[使用了django-treebeard的数据]
        """
        # 根据路径找到初始化文件【例如apps.users 下的MyUser模型，则路径为apps/users/fixtures/init_myuser.json】
        path_file = os.path.join(apps.get_app_config(self.app.split('.')[-1]).path, 'fixtures',
                                 f'init_{model._meta.model_name}.json')
        if not os.path.isfile(path_file):
            logger.info(f"文件不存在，跳过初始化:{path_file}")
            return
        with open(path_file, encoding="utf-8") as f:
            code_list = json.load(f)
        self.write_tree_structure(model, code_list, unique_fields=unique_fields)
        logger.info(f"[{self.app}][{model._meta.model_name}]初始化完成")

    def write_tree_structure(self, model, data, parent=None, unique_fields=None):
        """
        递归写入树形结构django-treebeard[没有关联外键就这样写，其他的分别单独处理]
        # 根据unique_fields判断是否已经存在
        """
        for item in data:
            children = item.pop('children', [])
            try:
                filter_data = {}
                # 配置过滤条件,如果有唯一标识字段则使用唯一标识字段，否则使用全部字段[重点-查找后会更新指定条目,没有则创建]
                if unique_fields:
                    for field in unique_fields:
                        if field in item:
                            filter_data[field] = item[field]
                else:
                    for key, value in item.items():
                        # 列表和空单独处理
                        if isinstance(value, list) or not value:
                            continue
                        filter_data[key] = value
                # logger.info(f"查找条件[{filter_data}]")
                instance = model.objects.get(**filter_data)
                for i, v in item.items():
                    # 列表和空单独处理
                    if isinstance(v, list) or not v:
                        continue
                    setattr(instance, i, v)
                # logger.info(f"更新[{instance}]")
                instance.save()
            except model.DoesNotExist:
                conditions = {}
                for key, value in item.items():
                    # 列表和空单独处理
                    if isinstance(value, list) or not value:
                        continue
                    conditions[key] = value
                if parent is None:
                    # logger.info(f"创建root[{conditions}]")
                    instance = model.add_root(**conditions)
                else:
                    # logger.info(f"创建child[{conditions}]")
                    instance = parent.add_child(**conditions)

            if children:
                self.write_tree_structure(model, children, parent=instance, unique_fields=unique_fields)

    def run(self):
        raise NotImplementedError('.run() must be overridden')
