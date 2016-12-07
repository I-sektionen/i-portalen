from django.http import HttpResponse

from .models import LetsEncrypt


def verification(request, url):
    content = str(LetsEncrypt.objects.get(url=url).text)

    response = HttpResponse(content, content_type='text/plain')
    response['Content-Length'] = len(content)

    return response