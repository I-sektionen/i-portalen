from django.core.urlresolvers import reverse
from django.template.loader_tags import register
from django.utils import timezone
from hero.models import Hero
from django.utils.translation import ugettext as _


@register.simple_tag()
def get_hero_url():
    heros = Hero.objects.filter(visible_from__lte=timezone.now())
    if heros.exists():
        return heros[0].file.url
    else:
        # Fallback
        return "https://s3.amazonaws.com/iportalen-us/static/iportalen/isektionen_logo.png"


@register.assignment_tag
def get_menu_choices_hero(user):
    menu_choices = []
    if user.has_perm("hero.change_hero"):
        menu_choices.append((_('Ändra hero'), reverse('iportalenadmin:app_list', args=('hero',))))

    return menu_choices
