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

from .models import Test,Inducation,Question,Option

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
        data['option'] = option
        data = dict_pagination_response(data, self.request, int(kwarg['page']), int(kwarg['page_size']))

        return data

    def format_data(self, data):
        if data is not None:
            return ok_json(data = data)


query_question_api = QuestionQueryAPI().wrap_func()