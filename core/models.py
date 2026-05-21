from django.db import models

class StudentProfile(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    branch = models.CharField(max_length=100)
    skills = models.TextField()

    def __str__(self):
        return self.name