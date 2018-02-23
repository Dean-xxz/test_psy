#__author__ = "Dean"
#__email__ = "1220543004@qq.com"

"""
此处提供up科技测试系统用户模块所需公共api
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

from .models import Wechat_user


#注册
class UserCreateAPI(AbstractAPI):
    def config_args(self):
        self.args = {
            'openid':'r',
            'unionid':'r',
            'nickname':'r',
            'sex':'r',
            'province':('o',None),
            'city':('o',None),
            'country':('o',None),
            'headimgurl':'r',
            'language':('o',None),
            'privilege':('o',None),
        }

    def access_db(self, kwarg):
        email = 'upupgogogo'+'163.com'
        password = '123456'
        openid = kwarg['openid']
        unionid = kwarg['unionid']
        nickname = kwarg['nickname']
        sex = kwarg['sex']
        province = kwarg['province']
        city = kwarg['city']
        country = kwarg['country']
        headimgurl = kwarg['headimgurl']
        language = kwarg['language']
        privilege = kwarg['privilege']


        try:
            user = Wechat_user.objects.get(openid = openid)
            wechat_user = Wechat_user.objects.filter(openid = openid).update(nickname = nickname,sex = sex,
                                                                             province = province,city = city,
                                                                             country = country,headimgurl = headimgurl,
                                                                             language = language,privilege = privilege)
            data = wechat_user.get_json()
            return data
        except Wechat_user.DoesNotExist:
            try:
                user = User.objects.get(username = nickname)
                nickname = nickname+'01'
                user = User.objects.create(username = nickname, email = email, password = password)
                user_id = user.id
                wechat_user = Wechat_user(user_id = user_id,openid = openid,unionid = unionid,nickname = nickname,province = province,
                                          country = country,headimgurl = headimgurl,language = language,privilege = privilege)
                wechat_user.save()
                if wechat_user:
                    data = wechat_user.get_json()
                    return data
                return 'create faild!'
            except User.DoesNotExist:
                user = User.objects.create(username=nickname, email=email, password=password)
                user_id = user.id
                wechat_user = Wechat_user(user_id=user_id, openid=openid, unionid=unionid, nickname=nickname,
                                          province=province,
                                          country=country, headimgurl=headimgurl, language=language,
                                          privilege=privilege)
                wechat_user.save()
                if wechat_user:
                    data = wechat_user.get_json()
                    return data
                return 'create faild!'

    def format_data(self, data):
        if data is not None:
            return ok_json(data = data)


create_user_api = UserCreateAPI().wrap_func()


class UserQueryAPI(AbstractAPI):
    def config_args(self):
        self.args = {
            'user_id':'r',
        }

    def access_db(self, kwarg):
        user_id = kwarg['user_id']
        try:
            user = Wechat_user.objects.get(user_id = user_id)
            data = user.get_json()
            return data
        except Wechat_user.DoesNotExist:
            return None

    def format_data(self, data):
        if data is not None:
            return ok_json(data = data)
        return fail_json('查无此人')


query_user_api = UserQueryAPI().wrap_func()