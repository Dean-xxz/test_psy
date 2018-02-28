import question.apis
from django.conf.urls import url

urlpatterns = [
    url(r'^test/query/$', question.apis.query_test_api, name="test_query_api"),
    url(r'^question/query/$', question.apis.query_question_api, name="question_query_api"),
    url(r'^inducation/query/$', question.apis.query_inducation_api, name="inducation_query_api"),
    url(r'^inducation/list/$', question.apis.list_inducation_api, name="inducation_list_api"),
    url(r'^result/create/$', question.apis.create_result_api, name="result_create_api"),
    url(r'^result/query/$', question.apis.query_result_api, name="result_query_api"),

]