from django.core.urlresolvers import reverse
from django.utils import timezone
from articles.models import Article
from organisations.models import Organisation
from django import template
from django.utils.translation import ugettext as _
register = template.Library()


@register.assignment_tag
def get_organisation_articles(organisation_pk):
    articles = Organisation.objects.get(pk=organisation_pk).article_set.filter(
        status=Article.APPROVED,
        visible_from__lte=timezone.now(),
        visible_to__gte=timezone.now()
    ).order_by('-visible_from')
    return articles


@register.assignment_tag
def get_menu_choices_article(user):
    menu_choices = []
    if user.article_set.filter(visible_to__gte=timezone.now()):
        menu_choices.append((_("Mina Artiklar"), reverse('articles:by user')))
    menu_choices.append((_("Skapa en artikel"), reverse('articles:create')))
    if user.has_perm("articles.can_approve_article"):
        menu_choices.append((_("Godkänn Artiklar"), reverse('articles:unapproved')))  # With perm to edit articles.
    return menu_choices
