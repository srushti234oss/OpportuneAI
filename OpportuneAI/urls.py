from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),
    path('scholarships/', views.scholarships, name='scholarships'),
    path('internships/', views.internships, name='internships'),
    path('hackathons/', views.hackathons, name='hackathons'),
    path('fellowships/', views.fellowships, name='fellowships'),
    path('tracker/', views.tracker, name='tracker'),
    path('skillmap/', views.skillmap, name='skillmap'),
]