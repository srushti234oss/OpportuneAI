from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

def scholarships(request):
    return render(request, 'scholarships.html')

def internships(request):
    return render(request, 'internships.html')

def hackathons(request):
    return render(request, 'hackathons.html')

def fellowships(request):
    return render(request, 'fellowships.html')

from .models import StudentProfile

def tracker(request):
    students = StudentProfile.objects.all()
    return render(request, 'tracker.html', {'students': students})

def skillmap(request):
    return render(request, 'skillmap.html')