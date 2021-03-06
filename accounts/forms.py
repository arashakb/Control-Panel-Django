from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Submission, Exercise, Solution, Student

class StudentForm(ModelForm):
	class Meta:
		model = Student
		fields = ['name', 'email', 'profile_pic']

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

class VideoForm(forms.ModelForm):
	class Meta:
		model = Submission
		fields = ['caption', 'video']

class ExerciseForm(forms.ModelForm):
	class Meta:
		model = Exercise
		fields = ['name', 'description']

class AnswerForm(forms.ModelForm):
	class Meta:
		model = Solution
		fields = ['studentsub', 'exercisesub', 'file']

class ScoreForm(forms.ModelForm):
	class Meta:
		model = Solution
		fields = ['mark']