from django.shortcuts import render
from .models import Opportunity
from .models import Scholarship
from .models import Hackathon
from .models import Fellowship
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import StudentProfile
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        User.objects.create_user(
            username=username,
            password=password
        )

        return redirect('/login/')

    return render(request, 'signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect('/')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('/')
def home(request):
    return render(request, 'index.html')

def scholarships(request):
    scholarships = Scholarship.objects.all()

    return render(request, 'scholarships.html', {
        'scholarships': scholarships
    })


def internships(request):
    opportunities = Opportunity.objects.filter(category="Internship")
    return render(request, 'internships.html', {'opportunities': opportunities})

def hackathons(request):
    hackathons = Hackathon.objects.all()

    return render(request, 'hackathons.html', {
        'hackathons': hackathons
    })

def fellowships(request):
    fellowships = Fellowship.objects.all()

    return render(request, 'fellowships.html', {
        'fellowships': fellowships
    })

from .models import StudentProfile

@login_required(login_url='/login/')
def tracker(request):

    saved_opportunities = Opportunity.objects.filter(
        saved_by=request.user,
        status='saved'
    )

    applied_opportunities = Opportunity.objects.filter(
        saved_by=request.user,
        status='applied'
    )

    accepted_opportunities = Opportunity.objects.filter(
        saved_by=request.user,
        status='accepted'
    )

    rejected_opportunities = Opportunity.objects.filter(
        saved_by=request.user,
        status='rejected'
    )

    return render(request, 'tracker.html', {
        'saved_opportunities': saved_opportunities,
        'applied_opportunities': applied_opportunities,
        'accepted_opportunities': accepted_opportunities,
        'rejected_opportunities': rejected_opportunities,
    })


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