from django.conf.urls import url
from . import views as faq_views
from django.contrib.auth.decorators import permission_required

urlpatterns = [
   url(r'^$',
       view=faq_views.topic_list,
       name='faq_topic_list',
       ),
   url(r'^(?P<slug>[\w-]+)/$',
       view=faq_views.topic_details,
       name='faq_topic_detail',
       ),
   url(r'^(?P<topic_slug>[\w-]+)/(?P<slug>[\w-]+)/$',
       view=faq_views.question_details,
       name='faq_question_detail',
       ),
   ]
