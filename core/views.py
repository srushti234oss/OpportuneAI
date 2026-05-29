from difflib import SequenceMatcher
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


def calculate_match_score(student_skills, required_skills):

    student_skills = student_skills.lower().split(',')

    required_skills = required_skills.lower().split(',')

    matched = 0

    for req_skill in required_skills:

        req_skill = req_skill.strip()

        for stu_skill in student_skills:

            stu_skill = stu_skill.strip()

            similarity = SequenceMatcher(
                None,
                stu_skill,
                req_skill
            ).ratio()

            if similarity > 0.6:
                matched += 1
                break

    if len(required_skills) == 0:
        return 0

    score = (matched / len(required_skills)) * 100

    return round(score, 2)


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

    opportunities = Opportunity.objects.all()

    profile = StudentProfile.objects.first()

    return render(request, 'index.html', {
        'opportunities': opportunities,
        'profile': profile,
    })



@login_required
def scholarships(request):

    scholarships = Opportunity.objects.filter(
        category="Scholarship"
    )

    return render(request,
                  'scholarships.html',
                  {'scholarships': scholarships})


@login_required
def internships(request):
    opportunities = Opportunity.objects.filter(category="Internship")
    return render(request, 'internships.html', {'opportunities': opportunities})

@login_required
def hackathons(request):

    hackathons = Opportunity.objects.filter(
        category="Hackathon"
    )

    return render(request,
                  'hackathons.html',
                  {'hackathons': hackathons})



@login_required
def fellowships(request):

    fellowships = Opportunity.objects.filter(
        category="Fellowship"
    )

    return render(request,
                  'fellowships.html',
                  {'fellowships': fellowships})



@login_required
def tracker(request):

    opportunities = Opportunity.objects.all()

    return render(request,
                  'tracker.html',
                  {'opportunities': opportunities})


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

    profile, created = StudentProfile.objects.get_or_create(
        user=request.user
    )

    context = {
        'profile': profile
    }

    return render(request, 'profile.html', context)


@login_required
def edit_profile(request):

    profile, created = StudentProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == 'POST':

        profile.full_name = request.POST.get('full_name')
        profile.branch = request.POST.get('branch')
        profile.skills = request.POST.get('skills')
        profile.cgpa = request.POST.get('cgpa')
        profile.bio = request.POST.get('bio')

        profile.save()

        return redirect('profile')

    return render(request, 'edit_profile.html', {
        'profile': profile
    })

