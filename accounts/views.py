from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, teacher_only
from .models import *
from .forms import *
# Create your views here.

@login_required(login_url='login')
def home(request):
    return render(request, 'accounts/dashboard.html')
@unauthenticated_user
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = UserCreationForm()
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
        context = {'form': form}
        return render(request, 'accounts/register.html', context)
@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('teacher_panel')
        else:
            messages.info(request, 'Username Or Password is incorrect')
    context = {}
    return render(request, 'accounts/login.html', context)

def logoutPage(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@teacher_only
def teacherPanel(request):
    exercises = Exercise.objects.all()
    total_exercises = exercises.count()
    videos = Submission.objects.all()
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('teacher_panel')
    else:
        form = VideoForm()
    context = {'exercises': exercises, 'total_exercises': total_exercises, 'videos': videos, 'form': form}
    return render(request, 'accounts/teacherpanel.html', context)

@login_required(login_url='login')
@teacher_only
def exerciseForm(request):
    if request.method == 'POST':
        form = ExerciseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('teacher_panel')
    else:
        form = ExerciseForm()
    context = {'form': form}
    return render(request, 'accounts/exercise_form.html', context)
@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def studentPanel(request):
    exercises = Exercise.objects.all()
    videos = Submission.objects.all()
    context = {'exercises': exercises, 'videos': videos}
    return render(request, 'accounts/studentpanel.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def accountSettings(request):
    student = request.user.student
    form = StudentForm(instance=student)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'accounts/account_settings.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['teacher'])
def exercise(request, pk):
    exercise = Exercise.objects.get(id=pk)
    students = Student.objects.all()
    solutions = exercise.solution_set.all()
    print(solutions)
    context = {'students': students, 'exercise': exercise, 'solutions': solutions}
    return render(request, 'accounts/exercises.html', context)
@login_required(login_url='login')
@allowed_users(allowed_roles=['teacher', 'student'])
def video(request, pk):
    video = Submission.objects.get(id=pk)
    context = {'video': video}
    return render(request, 'accounts/video.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def submitAnswer(request, pk):
    student = Solution.objects.get(id=pk)
    form = AnswerForm(instance=student)
    if request.method == 'POST':
        form = AnswerForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_panel')

    context = {'form': form}
    return render(request, 'accounts/submit_answer.html', context)