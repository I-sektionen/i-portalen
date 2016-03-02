from django.template.loader_tags import register
from django.utils import timezone
from hero.models import Hero


@register.simple_tag()
def get_hero_url():
    heros = Hero.objects.filter(visible_from__lte=timezone.now())
    if heros.exists():
        return heros[0].file.url
    else:
        # Fallback
        return "https://s3.amazonaws.com/iportalen-us/static/iportalen/isektionen_logo.png"
