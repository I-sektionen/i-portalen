from django.shortcuts import render

# Create your views here.
def evaluate_course(request):
    return render(request, "course_evaluations/evaluate_course.html", {})