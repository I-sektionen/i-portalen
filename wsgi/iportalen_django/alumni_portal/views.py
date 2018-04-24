from .models import Alumni_Article, Magazine
from django.shortcuts import render, redirect, get_object_or_404


def alumni_portal(request):
    articles = Alumni_Article.objects.published()
    return render(request, 'alumni_portal.html', {'articles': articles})


def alumni_magazine(request):
    magazines = Magazine.objects.order_by('-date')
    return render(request, 'alumni_magazine.html', {'magazines': magazines})


def single_article(request, pk):
    article = get_object_or_404(Alumni_Article, pk=pk)
    if article.can_administer(request.user):
        admin = True
    else:
        admin = False
    if article.show_article_before_experation or admin:
        # attachments = article.otherattachment_set
        # image_attachments = article.imageattachment_set
        return render(request, 'model/alumni_article.html', {
            'article': article,
            # 'attachments': attachments,
            # 'image_attachments': image_attachments,
            'can_administer': admin})
