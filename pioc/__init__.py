# coding: utf-8

import logging
import tornado.gen
from functools import wraps


class PIOC(object):
    _objects = {}
    _mapping = {}

    @classmethod
    def process_dependency(cls, *services):
        out = {}
        for service in services:
            logging.debug('get service: %s', service)
            inst = cls._objects.get(service, None)
            if not inst:
                cls_def, requirements = cls._mapping[service]
                logging.debug('init instance service %s with requirements: %s', service, requirements)
                inst = cls_def(**cls.process_dependency(*requirements)) if requirements else cls_def()
                cls._objects[service] = inst
            out[service] = inst
        return out

    @classmethod
    def service(cls, name, *requirements, **settings):
        def outer(cls_def):
            if name in cls._mapping:
                raise ValueError('%s already registered' % name)
            logging.debug('process inst: %s for service %s', requirements, name)
            cls._mapping[name] = (cls_def, requirements)
            if not settings.get('lazy', True):
                # 是否启用懒惰初始化
                # 继承关系无法使用lazy参数
                cls._objects[name] = cls_def(**cls.process_dependency(*requirements)) if requirements else cls_def()
            return cls_def

        return outer

    @classmethod
    def require(cls, *services):

        def outer(func):
            @wraps(func)
            def inner(*args, **kwargs):
                kwargs.update(cls.process_dependency(*services))
                return func(*args, **kwargs)

            return inner

        return outer

    @classmethod
    def require_co(cls, *services):

        def outer(func):
            @tornado.gen.coroutine
            @wraps(func)
            def inner(*args, **kwargs):
                kwargs.update(cls.process_dependency(*services))
                ret = yield func(*args, **kwargs)
                raise tornado.gen.Return(ret)

            return inner

        return outer

    @classmethod
    def destroy(cls):
        for inst in cls._objects.values():
            exit_func = getattr(inst, 'destroy', lambda: None)
            exit_func()
        cls._objects = {}

