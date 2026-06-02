from django.urls import path
from . import views
from .views import edit_profile
from .views import remove_opportunity
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('scholarships/', views.scholarships, name='scholarships'),
    path('internships/', views.internships, name='internships'),
    path('hackathons/', views.hackathons, name='hackathons'),
    path('fellowships/', views.fellowships, name='fellowships'),
    path('tracker/', views.tracker, name='tracker'),
    path('skillmap/', views.skillmap, name='skillmap'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('save/<int:id>/', views.save_opportunity, name='save_opportunity'),

    path('apply/<int:id>/', views.apply_opportunity, name='apply_opportunity'),

    path('accept/<int:id>/', views.accept_opportunity, name='accept_opportunity'),

    path('reject/<int:id>/', views.reject_opportunity, name='reject_opportunity'),

    path('remove/<int:id>/', views.remove_opportunity, name='remove_opportunity'),

    path('edit-profile/', edit_profile, name='edit_profile'),
    path('profile/', views.profile, name='profile'),
    path('profile/', views.profile, name='profile'),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
    path('update-note/<int:id>/', views.update_note, name='update_note'),
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
