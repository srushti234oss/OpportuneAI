from django.shortcuts import render
from .models import Opportunity
from .models import Scholarship
from .models import Hackathon
from .models import Fellowship
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, redirect
from django.contrib.auth.decorators import login_required
from .models import StudentProfile
def signup_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {
                "error": "Username already exists"
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)

        return redirect('/')

    return render(request, "signup.html")


def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('/')

        else:

            return render(request, "login.html", {
                "error": "Invalid credentials"
            })

    return render(request, "login.html")


def logout_view(request):

    logout(request)

    return redirect('/login/')
@login_required
def home(request):
    return render(request, 'index.html')
@login_required
def scholarships(request):
    scholarships = Scholarship.objects.all()

    return render(request, 'scholarships.html', {
        'scholarships': scholarships
    })
@login_required
def internships(request):
    opportunities = Opportunity.objects.filter(category="Internship")
    return render(request, 'internships.html', {'opportunities': opportunities})

@login_required
def hackathons(request):
    hackathons = Hackathon.objects.all()

    return render(request, 'hackathons.html', {
        'hackathons': hackathons
    })

@login_required
def fellowships(request):
    fellowships = Fellowship.objects.all()

    return render(request, 'fellowships.html', {
        'fellowships': fellowships
    })

from .models import StudentProfile

@login_required(login_url='/login/')
def tracker(request):

    saved_opportunities = Opportunity.objects.filter(saved_by=request.user)

    applied_opportunities = saved_opportunities.filter(status='applied')

    accepted_opportunities = saved_opportunities.filter(status='accepted')

    rejected_opportunities = saved_opportunities.filter(status='rejected')

    saved_opportunities = saved_opportunities.filter(status='saved')

    return render(request, 'tracker.html', {
        'saved_opportunities': saved_opportunities,
        'applied_opportunities': applied_opportunities,
        'accepted_opportunities': accepted_opportunities,
        'rejected_opportunities': rejected_opportunities,
    })


@login_required(login_url='/login/')
def skillmap(request):
    return render(request, 'skillmap.html')


@login_required(login_url='/login/')
def save_opportunity(request, id):

    opportunity = Opportunity.objects.get(id=id)

    opportunity.saved_by.add(request.user)

    return redirect('/tracker/')
@login_required
def remove_opportunity(request, id):
    opportunity = Opportunity.objects.get(id=id)

    opportunity.saved_by.remove(request.user)

    return redirect('/tracker/')
@login_required(login_url='/login/')
def apply_opportunity(request, id):

    opportunity = Opportunity.objects.get(id=id)

    opportunity.status = 'applied'

    opportunity.save()

    return redirect('/tracker/')


@login_required(login_url='/login/')
def accept_opportunity(request, id):

    opportunity = Opportunity.objects.get(id=id)

    opportunity.status = 'accepted'

    opportunity.save()

    return redirect('/tracker/')


@login_required(login_url='/login/')
def reject_opportunity(request, id):

    opportunity = Opportunity.objects.get(id=id)

    opportunity.status = 'rejected'

    opportunity.save()

    return redirect('/tracker/')
@login_required
def profile(request):

    profile = StudentProfile.objects.filter(user=request.user).first()

    return render(request, 'profile.html', {
        'profile': profile
    })
@login_required
def edit_profile(request):

    profile, created = StudentProfile.objects.get_or_create(
    user=request.user,
    defaults={
        'full_name': '',
        'branch': '',
        'skills': '',
        'cgpa': 0,
        'bio': '',
        'resume_link': ''
    }
)

    if request.method == "POST":

        profile.full_name = request.POST.get("full_name")

        profile.branch = request.POST.get("branch")

        profile.skills = request.POST.get("skills")

        profile.cgpa = request.POST.get("cgpa")

        profile.bio = request.POST.get("bio")

        profile.resume_link = request.POST.get("resume_link")
        if request.FILES.get('resume'):
            profile.resume = request.FILES.get('resume')
        
        profile.user = request.user
        profile.save()

        return redirect("/profile/")

    return render(request, "edit_profile.html", {
        "profile": profile
    })