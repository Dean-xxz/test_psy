from django.contrib import admin
from .models import Category,Test,Question,Inducation,Option,Result

# Register your models here.

admin.site.site_header = "小小志老师的精神病院收容所"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title','label','order')


admin.site.register(Category,CategoryAdmin)


class TestAdmin(admin.ModelAdmin):
    list_display = ('title','descp','order')
    list_filter = ('category',)


admin.site.register(Test,TestAdmin)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('number','stem','number')
    list_filter = ('inducation',)
    search_fields = ('number',)


admin.site.register(Question,QuestionAdmin)


class InducationAdmin(admin.ModelAdmin):
    list_display = ('title','order')
    list_filter = ('test',)


admin.site.register(Inducation,InducationAdmin)


class OptionAdmin(admin.ModelAdmin):
    list_display = ('title','order')
    list_filter = ('test',)


admin.site.register(Option,OptionAdmin)


class ResultAdmin(admin.ModelAdmin):
    list_display = ('question','user','score')


admin.site.register(Result,ResultAdmin)