from django.db import models

# Create your models here.

class Teacher(models.Model):
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class Student(models.Model):
    student_id = models.FloatField(null=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

class Exercise(models.Model):
    name = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=400, null=True)
