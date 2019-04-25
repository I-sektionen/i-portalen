from .models import Thesis_Article
from django.shortcuts import render, redirect, get_object_or_404


def thesis_portal(request):
    articles = Thesis_Article.objects.published()
    return render(request, 'thesis_portal.html', {'articles': articles})

def single_article(request, pk):
    article = get_object_or_404(Thesis_Article, pk=pk)
    if article.can_administer(request.user):
        admin = True
    else:
        admin = False
    if article.show_article_before_experation or admin:
        # attachments = article.otherattachment_set
        # image_attachments = article.imageattachment_set
        return render(request, 'model/thesis_article.html', {
            'article': article,
            # 'attachments': attachments,
            # 'image_attachments': image_attachments,
            'can_administer': admin})
