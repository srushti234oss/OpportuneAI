from django.contrib import admin
from .models import StudentProfile, Opportunity
from .models import Scholarship, Hackathon, Fellowship

admin.site.register(Scholarship)
admin.site.register(Hackathon)
admin.site.register(Fellowship)

admin.site.register(StudentProfile)
admin.site.register(Opportunity)