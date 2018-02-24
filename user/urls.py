import user.apis
from django.conf.urls import url

urlpatterns = [
    url(r'^create/$', user.apis.create_user_api, name="user_create_api"),
    url(r'^query/$', user.apis.query_user_api, name="user_query_api"),
    url(r'^openid/query/$', user.apis.query_openid_api, name="openid_query_api"),
]