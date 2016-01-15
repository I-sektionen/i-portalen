from django.contrib.auth.views import redirect_to_login
from django.shortcuts import get_object_or_404, render
from .models import Question, Topic, FAQ


def topic_list(request):
    return render(request, "faq/topic_list.html", {'faqs': FAQ.objects.all()})


def topic_details(request, slug):
    topic = Topic.objects.get(slug=slug)
    qs = topic.questions.all()
    if request.user.is_anonymous():
        qs = qs.exclude(protected=True)
    return render(request, "faq/topic_detail.html", {'topic': str(topic), 'questions': qs})


def question_details(request, topic_slug, slug):
    o = get_object_or_404(Question, slug=slug)
    if request.user.is_anonymous() and o.protected:
        return redirect_to_login(request.path)
    return render(request, "faq/question_detail.html", {'object': o})
