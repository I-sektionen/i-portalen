from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required()
def create_content(request):
    return render(request, "iportalen/create_content.html")
