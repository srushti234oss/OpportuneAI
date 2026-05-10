from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home, name='home'),
    path('scholarships/', scholarships, name='scholarships'),
    path('internships/', internships, name='internships'),
    path('hackathons/', hackathons, name='hackathons'),
    path('fellowships/', fellowships, name='fellowships'),
    path('tracker/', tracker, name='tracker'),
    path('skillmap/', skillmap, name='skillmap'),
]