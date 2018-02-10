import json
from django.db import models
from utils.basemodel.base import BaseModel
# from ckeditor.fields import RichTextField
# from ckeditor_uploader.fields import RichTextUploadingField
from django.core import serializers
from django.conf import settings

# Create your models here.

class Wechat_user(BaseModel):
    class Meta:
        verbose_name = "微信用户表"
        verbose_name_plural = "微信用户表"
        ordering = ["-create_time",]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="wechatuser")
    openid = models.CharField(max_length=50, blank=True, null=true, verbose_name=('OPENID'))
    unionid = models.CharField(max_length=50, verbose_name=('UNIONID'), unique=True,null = True,blank = True)
    nickname = models.CharField(max_length=50, verbose_name=('昵称'))
    sex = models.CharField(max_length=1, blank=True, null=True, verbose_name=('性别'))
    province = models.CharField(max_length=50, blank=True, null = True, verbose_name=('省份'))
    city = models.CharField(max_length=50, blank=True, verbose_name=('城市'))
    country = models.CharField(max_length=50, blank=True, null=True, verbose_name=('国家'))
    headimgurl = models.URLField(blank=True,null=True,verbose_name=('头像'))
    language = models.CharField(max_length=10, blank=True, null=True, verbose_name=('语言'))
    privilege = models.CharField(max_length=50, blank=True, null=True, verbose_name=('特权用户'))

    def __str__(self):
        return self.nickname

    def get_json(self):
        serials = serializers.serialize("json", [self])
        struct = json.loads(serials)
        data = struct[0]['fields']
        if 'pk' in struct[0]:
            data['id'] = struct[0]['pk']
        return data