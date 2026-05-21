from django.db import models
from django.contrib.auth.models import User

class StudentProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    full_name = models.CharField(max_length=200)

    branch = models.CharField(max_length=100)

    skills = models.TextField()

    cgpa = models.FloatField()

    bio = models.TextField()

    resume_link = models.URLField(blank=True)

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

    def __str__(self):
        return self.title
class Scholarship(models.Model):
    title = models.CharField(max_length=200)
    provider = models.CharField(max_length=200)
    description = models.TextField()
    deadline = models.CharField(max_length=100)

class Hackathon(models.Model):
    title = models.CharField(max_length=200)
    organizer = models.CharField(max_length=200)
    description = models.TextField()
    deadline = models.CharField(max_length=100)

class Fellowship(models.Model):
    title = models.CharField(max_length=200)
    organization = models.CharField(max_length=200)
    description = models.TextField()
    deadline = models.CharField(max_length=100)
STATUS_CHOICES = [
    ('saved', 'Saved'),
    ('applied', 'Applied'),
    ('accepted', 'Accepted'),
    ('rejected', 'Rejected'),
]

status = models.CharField(
    max_length=20,
    choices=STATUS_CHOICES,
    default='saved'
)