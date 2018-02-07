#coding=utf-8

import logging
import datetime

import utils.errors as err

from utils.view_tools import ok_json, fail_json, get_args
#from utils.timeutils import stamp_to_datetime

from django.db import models

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

class AbstractAPI(object):
    args = None

    def __init__(self):
        self.config_args()

    def config_args(self):
        self.args = {}

    def access_db(self, kwarg):
        return fail_json(err.ERROR_CODE_UNDEFINED)

    def format_data(self, data):
        if data is not None:
            if isinstance(data, models.query.QuerySet):
                return ok_json([d.get_json() for d in data])
            return ok_json(data.get_json())
        return fail_json(err.ERROR_CODE_DATABASE_ACCESS_ERROR)

    def wrap_func(self):
        def wrapper(request):
            args = get_args(request)
            self.request = request
            kwarg = {}
            for k in self.args:
                if self.args[k] == 'r' and k not in args:
                    return fail_json(err.ERROR_CODE_INVALID_ARGS, k)
                val = args.get(k, None)
                if not val:
                    val = self.args[k][1]
                kwarg[k] = val
            obj = self.access_db(kwarg)
            return self.format_data(obj)

        return wrapper


class ByIdQueryAbstractAPI(AbstractAPI):
    model = None
    def __init__(self, model=None):
        AbstractAPI.__init__(self)
        self.model = model

    def config_args(self):
        self.args = {'id': 'r'}

    def access_db(self, kwarg):
        if not self.model:
            return None
        try:
            obj = self.model.objects.get(pk=kwarg['id'], is_active=True)
            return obj
        except Exception as e:
            logger.error('[class:%s] %s' % (self.__class__.__name__, e))
            return None


class ByIdsQueryAbstractAPI(AbstractAPI):
    model = None
    def __init__(self, model=None):
        AbstractAPI.__init__(self)
        self.model = model

    def config_args(self):
        self.args = {'ids': 'r'}

    def access_db(self, kwarg):
        if not self.model:
            return None
        try:
            objs = self.model.objects.filter(id__in=kwarg['ids'].split(','), is_active=True)
            return objs
        except Exception as e:
            logger.error('[class:%s] %s' % (self.__class__.__name__, e))
            return None



class DeleteAbstractAPI(AbstractAPI):
    model = None
    def __init__(self, model=None):
        AbstractAPI.__init__(self)
        self.model = model

    def config_args(self):
        self.args = {'id': 'r'}

    def access_db(self, kwarg):
        if not self.model:
            return None
        try:
            obj = None
            if self.model.delete.__self__ is not None:
                obj = self.model.delete(id=kwarg['id'])
            else:
                obj = self.model.objects.get(pk=kwarg['id'], is_active=True)
                obj.is_active = False
                obj.save()
            return obj
        except Exception as e:
            logger.error('[class:%s] %s' % (self.__class__.__name__, e))
            return None

    def format_data(self, data):
        if not data:
            return fail_json(err.ERROR_CODE_DATABASE_DELETE_ERROR)
        return ok_json({'id':data.id})


class BatchDeleteAbstractAPI(AbstractAPI):
    model = None
    def __init__(self, model=None):
        AbstractAPI.__init__(self)
        self.model = model

    def config_args(self):
        self.args = {'ids': 'r'}

    def access_db(self, kwarg):
        if not self.model:
            return None
        try:
            ids = kwarg['ids']
            if type(ids) is not list:
                ids = ids.split(',')
            if self.model.delete.__self__ is not None:
                for id in ids:
                    self.model.delete(id=id)
                return ids
            else:
                self.model.objects.filter(pk__in=[int(id) for id in ids], is_active=True).update(is_active=False)
                return ids
        except Exception as e:
            logger.error('[class:%s] %s' % (self.__class__.__name__, e))
            return None

    def format_data(self, data):
        if not data:
            return fail_json(err.ERROR_CODE_DATABASE_DELETE_ERROR)
        return ok_json(data)


class UpdateAbstractAPI(AbstractAPI):
    model = None
    def __init__(self, model=None):
        AbstractAPI.__init__(self)
        self.model = model

    def config_args(self):
        self.args = {'id': 'r'}

    def access_db(self, kwarg):
        if not self.model:
            return None
        try:
            obj = self.model.objects.get(pk=kwarg['id'], is_active=True)
            for k in kwarg:
                if k is not 'id':
                    if type(obj.__dict__[k]) is datetime.datetime and type(kwarg[k]) is not datetime.datetime:
                        kwarg[k] = stamp_to_datetime(int(kwarg[k]))
                    if type(obj.__dict__[k]) is bool and type(kwarg[k]) is not bool:
                        kwarg[k] = str(kwarg[k]).lower() == 'true'
                    if kwarg[k] == '':
                        kwarg[k] = None
                    setattr(obj, k, kwarg[k])
            obj.save()
            return obj
        except Exception as e:
            logger.error('[class:%s] %s' % (self.__class__.__name__, e))
            return None

    def wrap_func(self):
        def wrapper(request):
            args = get_args(request)
            kwargs = {}
            for field in self.model._meta.fields:
                key_name = field.name
                if key_name in args:
                    kwargs[key_name] = args[key_name]
            obj = self.access_db(kwargs)
            return self.format_data(obj)
        return wrapper


class CreateAbstractAPI(AbstractAPI):
    model = None
    def __init__(self, model=None):
        AbstractAPI.__init__(self)
        self.model = model

    def config_args(self):
        self.args = {}

    def access_db(self, kwarg):
        if not self.model:
            return None
        try:
            obj = self.model()
            for k in kwarg:
                if type(obj.__dict__[k]) is datetime.datetime and type(kwarg[k]) is not datetime.datetime:
                    kwarg[k] = stamp_to_datetime(int(kwarg[k]))
                if type(obj.__dict__[k]) is bool and type(kwarg[k]) is not bool:
                    kwarg[k] = str(kwarg[k]).lower() == 'true'
                if type(obj.__dict__[k]) is int and type(kwarg[k]) is not int:
                    kwarg[k] = int(kwarg[k])
                setattr(obj, k, kwarg[k])
            obj.save()
            return obj
        except Exception as e:
            logger.error('[class:%s] %s' % (self.__class__.__name__, e))
            return None

    def wrap_func(self):
        def wrapper(request):
            args = get_args(request)
            kwargs = {}
            for field in self.model._meta.fields:
                if field.name in ['create_time', 'update_time', 'is_active']:
                    continue
                key_name = field.column
                if not field.null and key_name not in args and key_name is not 'id':
                    return fail_json(err.ERROR_CODE_INVALID_ARGS, field.name)
                if key_name in args:
                    kwargs[key_name] = args[key_name]
            obj = self.access_db(kwargs)
            return self.format_data(obj)
        return wrapper


class AssitListOrderAbstractAPI(AbstractAPI):
    model = None
    def __init__(self, model=None):
        AbstractAPI.__init__(self)
        self.model = model

    def config_args(self):
        self.args = {'parent_id': 'r',
                'target_id': 'r',
                'index': 'r'}

    def access_db(self, kwarg):
        if not self.model:
            return None
        try:
            obj = self.model.update(int(kwarg['parent_id']), int(kwarg['target_id']), int(kwarg['index']))
            return obj
        except Exception as e:
            logger.error('[class:%s] %s' % (self.__class__.__name__, e))
            return None

    def format_data(self, data):
        if not data:
            return fail_json(err.ERROR_CODE_DATABASE_DELETE_ERROR)
        return ok_json(data)
