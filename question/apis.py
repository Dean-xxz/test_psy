#__author__ = "Dean"
#__email__ = "1220543004@qq.com"

"""
此处提供up科技测试系统题目模块所需公共api
"""
import json
import datetime

from django.conf import settings
from django.core import serializers
from django.db.models import Q

from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login

from utils.paginator import json_pagination_response, dict_pagination_response
from utils.view_tools import ok_json, fail_json,get_args
from utils.abstract_api import AbstractAPI

from .models import Test,Inducation,Question,Option,Result
from .utils import get_inducation_avg

# 测试信息展示接口


class TestQueryAPI(AbstractAPI):
    def config_args(self):
        self.args = {
            'test_id':'r',
        }

    def access_db(self, kwarg):
        test_id = kwarg['test_id']

        try:
            test = Test.objects.get(pk = test_id)
            data = test.get_json()
            return data
        except Test.DoesNotExist:
            return None

    def format_data(self, data):
        if data is not None:
            return ok_json(data = data)
        return fail_json('test is does not exit')


query_test_api = TestQueryAPI().wrap_func()


# 测试题目展示接口
class QuestionQueryAPI(AbstractAPI):
    def config_args(self):
        self.args = {
            'test_id':'r',
            'page': ('o', 1),
            'page_size': ('o', 1),
        }

    def access_db(self, kwarg):
        test_id = kwarg['test_id']

        test = Question.objects.filter(test_id = test_id)
        data = [o.get_json() for o in test]
        option = Option.objects.filter(test_id = test_id)
        option = [o.get_json() for o in option]
        for i in data:
            i['option'] = option
        # data['option'] = option
        data = dict_pagination_response(data, self.request, int(kwarg['page']), int(kwarg['page_size']))

        return data

    def format_data(self, data):
        if data is not None:
            return ok_json(data = data)


query_question_api = QuestionQueryAPI().wrap_func()


# 类型列表
class InducationListAPI(AbstractAPI):
    def config_args(self):
        self.args = {

        }

    def access_db(self, kwarg):


        data = Inducation.objects.filter(test_id = 1)
        data = [o.get_json() for o in data]


        return data

    def format_data(self, data):
        if data is not None:
            return ok_json(data = data)



list_inducation_api = InducationListAPI().wrap_func()


# 单一分类查询

class InducationQueryAPI(AbstractAPI):
    def config_args(self):
        self.args = {
            "inducation_id":'r',
        }

    def access_db(self, kwarg):
        inducation_id = kwarg['inducation_id']

        try:
            data = Inducation.objects.get(pk = inducation_id)
            data = data.get_json()
            return data
        except Inducation.DoesNotExist:
            return None

    def format_data(self, data):
        if data is not None:
            return ok_json(data = data)
        return fail_json('inducation is not exit')


query_inducation_api = InducationQueryAPI().wrap_func()


# 用户测试结果创建接口
class ResultCreateAPI(AbstractAPI):
    def config_args(self):
        self.args = {
            "user_id":'r',
            "data":'r',
        }

    def access_db(self, kwarg):
        user_id = kwarg['user_id']
        data = kwarg['data']

        data = eval(data)
        for key, value in data.items():
            user_id = user_id
            question_id = key
            score = data[key]
            result = Result(user_id = user_id,question_id = question_id,score = score)
            result.save()

        return 'save successful'

    def format_data(self, data):
        return ok_json(data = data)


create_result_api = ResultCreateAPI().wrap_func()


# 用户测试结果查询
class ResultQueryAPI(AbstractAPI):
    def config_args(self):
        self.args = {
            "user_id":'r',
        }

    def access_db(self, kwarg):
        user_id = kwarg['user_id']

        #查询分类列表
        inducation_list = Inducation.objects.filter(test_id=1)
        data = [o.get_json() for o in inducation_list]
        #计算每个分类得分
        for i in data:
            inducation_id = i['id']
            i['avg'] = get_inducation_avg(inducation_id = inducation_id,user_id = user_id)
        #根据分值排序返回结果
        data = data.sort(key=lambda k: (k.get('avg', 0)))

        return data
    def format_data(self, data):
        return ok_json(data = data)


query_result_api = ResultQueryAPI().wrap_func()