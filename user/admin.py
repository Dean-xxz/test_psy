from django.contrib import admin
from .models import Wechat_user

# Register your models here.

class WechatUserAdmin(admin.ModelAdmin):
    list_display = ('user','nickname','openid','unionid','sex','province','city','country','language','privilege')
    search_fields = ('nickname',)

admin.site.register(Wechat_user,WechatUserAdmin)