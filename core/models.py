from django.db import models
from django.contrib.auth.models import User


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    year = models.CharField(max_length=20, blank=True, default='')
    college = models.CharField(max_length=200, blank=True, default='')
    full_name = models.CharField(max_length=200, blank=True, default='')
    branch = models.CharField(max_length=100, blank=True, default='')
    skills = models.TextField(blank=True, default='')
    cgpa = models.FloatField(default=0.0)
    bio = models.TextField(blank=True, default='')
    resume_link = models.URLField(blank=True, default='')
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)

    def __str__(self):
        return self.full_name


class Opportunity(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateField()
    saved_by = models.ManyToManyField(User, blank=True)
    status = models.CharField(max_length=20, default='saved')
    required_skills = models.TextField(blank=True)

    minimum_cgpa = models.FloatField(default=0)

    ai_category = models.CharField(
    max_length=100,
    blank=True
    )

    def __str__(self):
        return self.title
    
class Scholarship(models.Model):
    title = models.CharField(max_length=255)
    provider = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.CharField(max_length=100)

    required_skills = models.CharField(
        max_length=500,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title
    
class Hackathon(models.Model):
    title = models.CharField(max_length=255)
    organizer = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.CharField(max_length=100)

    required_skills = models.CharField(
        max_length=500,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title

class Fellowship(models.Model):
    title = models.CharField(max_length=200)
    organization = models.CharField(max_length=200)
    description = models.TextField()
    deadline = models.CharField(max_length=100)
    required_skills = models.CharField(max_length=300, default="")
    minimum_cgpa = models.FloatField(default=0.0)
    ai_category = models.CharField(max_length=100, default="Research")

    def __str__(self):
        return self.title

class SavedOpportunity(models.Model):
    STATUS_CHOICES = [
        ('saved', 'Saved'),
        ('applied', 'Applied'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='saved')
    saved_at = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True, default='')  # ← ADD THIS LINE

    def __str__(self):
        return f"{self.user.username} - {self.opportunity.title}"