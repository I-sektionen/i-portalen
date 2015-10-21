from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required()
def create_content(request):
    return render(request, "iportalen/create_content.html")

@login_required()
def approve_content(request):
    return render(request, "iportalen/approve_content.html")

def placeholder(request):
    return render(request, "placeholder.html")
