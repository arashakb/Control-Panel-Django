from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Exercise(models.Model):
    name = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=400, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.name
class Teacher(models.Model):
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    student_id = models.IntegerField(null=True)
    name = models.CharField(max_length=200, null=True)
    photo = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    exercises = models.ManyToManyField(Exercise)

    def __str__(self):
        return self.name


