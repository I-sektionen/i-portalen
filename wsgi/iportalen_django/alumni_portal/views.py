from django.shortcuts import render


def alumni_portal(request):
    print("!!!!!")
    return render(request, 'alumni_portal.html')

