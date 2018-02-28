import json
from django.db import models
from django.conf import settings
from utils.basemodel.base import BaseModel
# from ckeditor.fields import RichTextField
# from ckeditor_uploader.fields import RichTextUploadingField
from django.core import serializers
from django.contrib.auth.models import User
from user.models import Wechat_user

# Create your models here.

class Category(BaseModel):
    class Meta:
        verbose_name = "测试类别"
        verbose_name_plural = "测试类别"
        ordering = ["order",]

    title = models.CharField(max_length=128,verbose_name="分类标题")
    label = models.CharField(max_length=128,verbose_name="分类标签",null=True,blank=True)
    image = models.ImageField(upload_to="media/question/category/",verbose_name="分类图片",null=True,blank=True)
    order = models.PositiveSmallIntegerField(verbose_name = "顺序",default = 1,help_text = "该分类在列表中的顺序")
    remarks = models.TextField(verbose_name="备注、描述",null=True,blank=True,help_text="请输入这类行测试的描述等")

    def __str__(self):
        return self.title

    def get_json(self):
        serials = serializers.serialize("json", [self])
        struct = json.loads(serials)
        data = struct[0]['fields']
        if 'pk' in struct[0]:
            data['id'] = struct[0]['pk']
        return data


class Test(BaseModel):
    class Meta:
        verbose_name="测试"
        verbose_name_plural='测试'
        ordering=['order',]

    category = models.ForeignKey("Category",verbose_name="所属测试类别",related_name="test_category")
    title = models.CharField(max_length=128,verbose_name="测试名称")
    image = models.ImageField(upload_to="media/question/test/", verbose_name="测试介绍图片", null=True, blank=True)
    descp = models.TextField(verbose_name="测试描述",null=True,blank=True)
    order = models.PositiveSmallIntegerField(verbose_name="顺序", default=1,help_text="该测试在测试列表中的顺序")

    def __str__(self):
        return self.title

    def get_json(self):
        serials = serializers.serialize("json", [self])
        struct = json.loads(serials)
        data = struct[0]['fields']
        if 'pk' in struct[0]:
            data['id'] = struct[0]['pk']
        return data


class Inducation(BaseModel):
    class Meta:
        verbose_name="结果分类"
        verbose_name_plural="结果分类"
        ordering=['order',]

    test = models.ForeignKey("Test", verbose_name="所属测试", related_name="inducation_test")
    title = models.CharField(max_length=128,verbose_name="类型名称")
    label = models.CharField(max_length=128,verbose_name="类型标签",null=True,blank=True)
    color = models.CharField(max_length=128,verbose_name="类型颜色",null=True,blank=True)
    image = models.ImageField(upload_to="media/question/inducation/", verbose_name="类型卡片", null=True, blank=True)
    descp = models.TextField(verbose_name="类型描述", null=True, blank=True)
    order = models.PositiveSmallIntegerField(verbose_name="顺序", default=1, help_text="该类型在分类列表中的顺序")

    def __str__(self):
        return self.title

    def get_json(self):
        serials = serializers.serialize("json", [self])
        struct = json.loads(serials)
        data = struct[0]['fields']
        if 'pk' in struct[0]:
            data['id'] = struct[0]['pk']
        return data


class Question(BaseModel):
    class Meta:
        verbose_name="题目"
        verbose_name_plural="题目"
        ordering=['number',]

    test = models.ForeignKey("Test", verbose_name="所属测试", related_name="question_test",null=True,blank=True)
    inducation = models.ForeignKey("Inducation", verbose_name="所属结果分类", related_name="question_inducation")
    number = models.PositiveSmallIntegerField(verbose_name="题号", default=1, help_text="题目的题号")
    stem = models.CharField(max_length=512,verbose_name="题干")
    remarks = models.TextField(verbose_name="备注",null=True,blank=True)

    def __str__(self):
        return self.stem

    def get_json(self):
        serials = serializers.serialize("json", [self])
        struct = json.loads(serials)
        data = struct[0]['fields']
        if 'pk' in struct[0]:
            data['id'] = struct[0]['pk']
        return data


class Option(BaseModel):
    class Meta:
        verbose_name="题目选项"
        verbose_name_plural="题目选项"
        ordering=['order',]

    test = models.ForeignKey("Test", verbose_name="所属测试", related_name="option_test")
    title = models.CharField(max_length=128,verbose_name="选项")
    descp = models.TextField(verbose_name="备注",null=True,blank=True)
    order = models.PositiveSmallIntegerField(verbose_name="顺序", default=1, help_text="该选项在列表中的顺序")

    def __str__(self):
        return self.title

    def get_json(self):
        serials = serializers.serialize("json", [self])
        struct = json.loads(serials)
        data = struct[0]['fields']
        if 'pk' in struct[0]:
            data['id'] = struct[0]['pk']
        return data


class Result(BaseModel):
    class Meta:
        verbose_name="测试记录表"
        verbose_name_plural="测试记录表"
        ordering=['question',]

    question = models.ForeignKey("Question", verbose_name="题目题号", related_name="result_question")
    score = models.IntegerField(verbose_name="分值",blank=True,null =True)
    user = models.ForeignKey("user.Wechat_user", verbose_name="测试人", related_name="result_user")

    def __str__(self):
        return self.question,self.score,self.user

    def get_json(self):
        serials = serializers.serialize("json", [self])
        struct = json.loads(serials)
        data = struct[0]['fields']
        if 'pk' in struct[0]:
            data['id'] = struct[0]['pk']
        return data