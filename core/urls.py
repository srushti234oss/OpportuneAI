from django.urls import path
from . import views
from .views import remove_opportunity

urlpatterns = [
    path('', views.home, name='home'),
    path('scholarships/', views.scholarships, name='scholarships'),
    path('internships/', views.internships, name='internships'),
    path('hackathons/', views.hackathons, name='hackathons'),
    path('fellowships/', views.fellowships, name='fellowships'),
    path('tracker/', views.tracker, name='tracker'),
    path('skillmap/', views.skillmap, name='skillmap'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('save/<int:id>/', views.save_opportunity),
    path('apply/<int:id>/', views.apply_opportunity),
    path('accept/<int:id>/', views.accept_opportunity),
    path('reject/<int:id>/', views.reject_opportunity),
    path('remove/<int:id>/', views.remove_opportunity),
]