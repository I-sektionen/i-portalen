from django.conf.urls import url, include
from . import views

app_name = "faq"

faq_patterns = [
    url(r'^$',                                         view=views.topic_list,       name='faq_topic_list'),
    url(r'^(?P<slug>[\w-]+)/$',                        view=views.topic_details,    name='faq_topic_detail'),
    url(r'^(?P<topic_slug>[\w-]+)/(?P<slug>[\w-]+)/$', view=views.question_details, name='faq_question_detail'),
]

urlpatterns = [url(r'^', include(faq_patterns, namespace=app_name))]
