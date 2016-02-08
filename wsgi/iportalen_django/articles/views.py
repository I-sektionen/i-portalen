from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db import transaction
from django.utils.translation import ugettext as _
from .models import Article
from .forms import ArticleForm, RejectionForm
from django.forms import modelformset_factory
import mimetypes
from .models import Article, OtherAttachment, ImageAttachment
from .forms import ArticleForm, RejectionForm, AttachmentForm, ImageAttachmentForm
from tags.models import Tag


@login_required()
def create_or_modify_article(request, pk=None):  # TODO: Reduce complexity
    if pk:  # if pk is set we modify an existing article.
        duplicates = Article.objects.filter(replacing_id=pk)
        if duplicates:
            links = ""
            for d in duplicates:
                links += "<a href='{0}'>{1}</a><br>".format(d.get_absolute_url(), d.headline)
            messages.error(
                request,
                "".join([_("Det finns redan en ändrad version av det här arrangemanget!"
                           " Är du säker på att du vill ändra den här?"
                           "<br>Följande ändringar är redan föreslagna:"),
                         " <br> {:}"]).format(links),
                extra_tags='safe')
        article = get_object_or_404(Article, pk=pk)
        if not article.can_administer(request.user):
            return HttpResponseForbidden()
        form = ArticleForm(request.POST or None, request.FILES or None, instance=article)
    else:  # new article.
        form = ArticleForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            article = form.save(commit=False)

            if form.cleaned_data['draft']:
                draft = True
            else:
                draft = False

            status = article.get_new_status(draft)
            article.status = status["status"]
            article.user = request.user

            if status["new"]:
                article.replacing_id = article.id
                article.id = None

            article.save()
            form.save_m2m()
            if article.status == Article.DRAFT:
                messages.success(request, _("Dina ändringar har sparats i ett utkast."))
            elif article.status == Article.BEING_REVIEWED:
                messages.success(request, _("Dina ändringar har skickats för granskning."))
            return redirect('articles:article', pk=article.pk)
        else:
            messages.error(request, _("Det uppstod ett fel, se detaljer nedan."))
            return render(request, 'articles/article_form.html', {
                'form': form,
            })
    return render(request, 'articles/article_form.html', {
        'form': form,
    })


def upload_attachments(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if not article.can_administer(request.user):
        return HttpResponseForbidden()
    AttachmentFormset = modelformset_factory(OtherAttachment,
                                             form=AttachmentForm,
                                             max_num=30,
                                             extra=3,
                                             can_delete=True,
                                             )
    if request.method == 'POST':
        formset = AttachmentFormset(request.POST, request.FILES, queryset=OtherAttachment.objects.filter(article=article))
        if formset.is_valid():
            for entry in formset.cleaned_data:
                if not entry == {}:
                    if entry['DELETE']:
                        entry['id'].delete()  # TODO: Remove the clear option from html-widget (or make it work).
                    else:
                        if entry['id']:
                            attachment = entry['id']
                        else:
                            attachment = OtherAttachment(article=article)
                            attachment.file_name = entry['file'].name
                        attachment.file = entry['file']
                        attachment.display_name = entry['display_name']
                        attachment.modified_by = request.user
                        attachment.save()
            messages.success(request, 'Dina bilagor har sparats.')
            return redirect('articles:manage attachments', article_pk=article.pk)
        else:
            return render(request, "articles/attachments.html", {
                        'article': article,
                        'formset': formset,
                        })
    formset = AttachmentFormset(queryset=OtherAttachment.objects.filter(article=article))
    return render(request, "articles/attachments.html", {
                        'article': article,
                        'formset': formset,
                        })


def upload_attachments_images(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if not article.can_administer(request.user):
        return HttpResponseForbidden()
    AttachmentFormset = modelformset_factory(ImageAttachment,
                                             form=ImageAttachmentForm,
                                             max_num=30,
                                             extra=3,
                                             can_delete=True,
                                             )
    if request.method == 'POST':
        formset = AttachmentFormset(request.POST,
                                    request.FILES,
                                    queryset=ImageAttachment.objects.filter(article=article)
                                    )
        if formset.is_valid():
            for entry in formset.cleaned_data:
                if not entry == {}:
                    if entry['DELETE']:
                        entry['id'].delete()  # TODO: Remove the clear option from html-widget (or make it work).
                    else:
                        if entry['id']:
                            attachment = entry['id']
                        else:
                            attachment = ImageAttachment(article=article)
                        attachment.img = entry['img']
                        attachment.caption = entry['caption']
                        attachment.modified_by = request.user
                        attachment.save()
            messages.success(request, 'Dina bilagor har sparats.')
            return redirect('articles:article', article.pk)
        else:
            return render(request, "articles/attach_images.html", {
                        'article': article,
                        'formset': formset,
                        })
    formset = AttachmentFormset(queryset=ImageAttachment.objects.filter(article=article))
    return render(request, "articles/attach_images.html", {
                        'article': article,
                        'formset': formset,
                        })


def download_attachment(request, pk):
    attachment = OtherAttachment.objects.get(pk=pk)
    mimetype, enc = mimetypes.guess_type(attachment.file.url)
    response = HttpResponse(attachment.file, content_type=mimetype)
    response['Content-Disposition'] = 'attachment; filename="{filename}"'.format(filename=attachment.file_name)
    return response


def single_article(request, pk):
    article = Article.objects.get(pk=pk)
    if article.can_administer(request.user):
        admin = True
    else:
        admin = False
    if article.status == Article.APPROVED or admin:
        attachments = article.otherattachment_set
        image_attachments = article.imageattachment_set
        return render(request, 'articles/article.html', {
            'article': article,
            'attachments': attachments,
            'image_attachments': image_attachments,
            'can_administer': admin})
    raise PermissionDenied


def all_articles(request):
    articles = Article.objects.published()
    return render(request, 'articles/articles.html', {'articles': articles})


@login_required()
def all_unapproved_articles(request):
    if request.user.has_perm("articles.can_approve_article"):
        articles = Article.objects.filter(status=Article.BEING_REVIEWED, visible_to__gte=timezone.now())
        return render(request, 'articles/approve_articles.html', {'articles': articles})
    else:
        raise PermissionDenied


@login_required()
@transaction.atomic
def approve_article(request, pk):
    article = Article.objects.get(pk=pk)
    if article.approve(request.user):
        return redirect('articles:unapproved')
    else:
        raise PermissionDenied


@login_required()
def unapprove_article(request, pk):
    article = Article.objects.get(pk=pk)
    form = RejectionForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            if article.reject(request.user, form.cleaned_data['rejection_message']):
                messages.success(request, _("Artikeln har avslagits."))
                return redirect('articles:unapproved')
            else:
                raise PermissionDenied
    return render(request, 'articles/reject.html', {'form': form, 'article': article})


def articles_by_tag(request, tag_name):
    articles = Tag.objects.get(name=tag_name).article_set.filter(status=Article.APPROVED)
    return render(request, 'articles/articles.html', {'articles': articles})


@login_required()
def articles_by_user(request):
    user_articles = request.user.article_set.filter(visible_to__gte=timezone.now()).order_by('-visible_from')
    user_org = request.user.get_organisations()

    for o in user_org:
        user_articles |= o.article_set.filter(visible_to__gte=timezone.now()).order_by('-visible_from')

    return render(request, 'articles/my_articles.html',
                  {'user_articles': user_articles.order_by('-visible_from').distinct()})


@login_required()
def delete_article(request, pk):
    article = Article.objects.get(pk=pk)

    if article.draft and request.user == article.user:
        article.delete()
        return redirect('articles:by user')
    raise PermissionDenied

