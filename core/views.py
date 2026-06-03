
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
from .ai_engine import get_recommended_opportunities
from .ai_engine import get_recommended_fellowships
from .ai_engine import get_recommended_scholarships
from .ai_engine import get_recommended_hackathons
from .models import SavedOpportunity

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

    profile = StudentProfile.objects.filter(
        user=request.user
    ).first()

    recommendations = []

    if profile:
        recommendations = get_recommended_opportunities(
            profile
        )

    return render(request, 'index.html', {
        'recommendations': recommendations,
        'profile': profile
    })




@login_required
def scholarships(request):

    student = StudentProfile.objects.get(user=request.user)

    recommendations = get_recommended_scholarships(student)

    return render(request, 'scholarships.html', {
        'recommendations': recommendations
    })


@login_required
def internships(request):

    student = StudentProfile.objects.get(user=request.user)

    recommendations = get_recommended_opportunities(student)

    return render(request, 'internships.html', {
        'recommendations': recommendations
    })

@login_required
def hackathons(request):

    student = StudentProfile.objects.get(user=request.user)

    recommendations = get_recommended_hackathons(student)

    return render(request, 'hackathons.html', {
        'recommendations': recommendations
    })

@login_required
def fellowships(request):

    student = StudentProfile.objects.get(user=request.user)

    recommendations = get_recommended_fellowships(student)

    return render(request, 'fellowships.html', {
        'recommendations': recommendations
    })

from .models import StudentProfile

@login_required(login_url='/login/')
def tracker(request):

    saved_opportunities = SavedOpportunity.objects.filter(
        user=request.user
    )

    saved = saved_opportunities.filter(status='saved')

    applied = saved_opportunities.filter(status='applied')

    accepted = saved_opportunities.filter(status='accepted')

    rejected = saved_opportunities.filter(status='rejected')

    return render(request, 'tracker.html', {

        'saved_opportunities': saved,

        'applied_opportunities': applied,

        'accepted_opportunities': accepted,

        'rejected_opportunities': rejected,
    })

@login_required(login_url='/login/')
def skillmap(request):
    return render(request, 'skillmap.html')


@login_required(login_url='/login/')
def save_opportunity(request, id):
 opportunity = Opportunity.objects.get(id=id)
 SavedOpportunity.objects.create(
    user=request.user,
    opportunity=opportunity,
    status='saved'
    )
 return redirect('/tracker/')

@login_required
def remove_opportunity(request, id):

    item = SavedOpportunity.objects.get(id=id)

    item.delete()

    return redirect('/tracker/')


@login_required
def apply_opportunity(request, id):

    item = SavedOpportunity.objects.get(id=id)

    item.status = 'applied'

    item.save()

    return redirect('/tracker/')

@login_required
def accept_opportunity(request, id):

    item = SavedOpportunity.objects.get(id=id)

    item.status = 'accepted'

    item.save()

    return redirect('/tracker/')


@login_required
def reject_opportunity(request, id):

    item = SavedOpportunity.objects.get(id=id)

    item.status = 'rejected'

    item.save()

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