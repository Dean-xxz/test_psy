import question.apis
from django.conf.urls import url

urlpatterns = [
    url(r'^test/query/$', question.apis.query_test_api, name="test_query_api"),
    url(r'^question/query/$', question.apis.query_question_api, name="question_query_api"),
]