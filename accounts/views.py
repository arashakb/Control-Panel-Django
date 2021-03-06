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
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.


class Home(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'accounts/dashboard.html')


class LoginView(View):
    @method_decorator(unauthenticated_user)
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('teacher_panel')
        else:
            messages.info(request, 'Username Or Password is incorrect')

    @method_decorator(unauthenticated_user)
    def get(self, request):
        return render(request, 'accounts/login.html')

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


class TeacherPanel(View):
    form_class = VideoForm
    exercises = Exercise.objects.all()
    total_exercises = exercises.count()
    videos = Submission.objects.all()

    @method_decorator(login_required)
    @method_decorator(teacher_only)
    def get(self, request, *args, **kwargs):
        form = self.form_class()

        context = {'exercises': self.exercises, 'total_exercises': self.total_exercises, 'videos': self.videos, 'form': form}
        return render(request, 'accounts/teacherpanel.html', context)

    @method_decorator(login_required)
    @method_decorator(teacher_only)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        video_name = request.FILES['video'].name
        if '.mp4' in video_name:
            if form.is_valid():
                form.save()
                return redirect('teacher_panel')
        else:
            return redirect('bad_type')

        context = {'exercises': self.exercises, 'total_exercises': self.total_exercises, 'videos': self.videos, 'form': form}
        return render(request, 'accounts/teacherpanel.html', context)

class ExerciseForm(View):
    form_class = ExerciseForm

    @method_decorator(login_required)
    @method_decorator(teacher_only)
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, 'accounts/exercise_form.html', {'form': form})

    @method_decorator(login_required)
    @method_decorator(teacher_only)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('teacher_panel')
        return render(request, 'accounts/exercise_form.html', {'form': form})

class StudentPanel(View):
    exercises = Exercise.objects.all()
    videos = Submission.objects.all()

    @method_decorator(allowed_users(allowed_roles=['student']))
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = {'exercises': self.exercises, 'videos': self.videos}
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


class ExerciseView(View):

    @method_decorator(login_required)
    @method_decorator(allowed_users(allowed_roles=['teacher']))
    def get(self, request, pk, *args, **kwargs):
        exercise = Exercise.objects.get(id=pk)
        students = Student.objects.all()
        solutions = exercise.solution_set.all()
        context = {'students': students, 'exercise': exercise, 'solutions': solutions}
        return render(request, 'accounts/exercises.html', context)


class VideoView(View):

    @method_decorator(login_required)
    @method_decorator(allowed_users(allowed_roles=['teacher', 'student']))
    def get(self, request, pk, *args, **kwargs):
        video = Submission.objects.get(id=pk)
        context = {'video': video}
        return render(request, 'accounts/video.html', context)

class SubmitAnswer(View):
    form_class = AnswerForm

    @method_decorator(login_required)
    @method_decorator(allowed_users(allowed_roles=['student']))
    def get(self, request, pk, *args, **kwargs):
        student = Solution.objects.get(id=pk)
        form = self.form_class(instance=student)
        return render(request, 'accounts/submit_answer.html', {'form': form})

    @method_decorator(login_required)
    @method_decorator(allowed_users(allowed_roles=['student']))
    def post(self, request, pk, *args, **kwargs):
        student = Solution.objects.get(id=pk)
        form = self.form_class(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_panel')
        return render(request, 'accounts/submit_answer.html', {'form': form})


class GivingScore(View):
    form_class = ScoreForm

    @method_decorator(login_required)
    @method_decorator(allowed_users(allowed_roles=['teacher']))
    def get(self, request, pk, *args, **kwargs):
        score = Solution.objects.get(id=pk)
        form = self.form_class(instance=score)
        return render(request, 'accounts/giving_score.html', {'form': form})

    @method_decorator(login_required)
    @method_decorator(allowed_users(allowed_roles=['teacher']))
    def post(self, request, pk, *args, **kwargs):
        score = Solution.objects.get(id=pk)
        form = self.form_class(request.POST, request.FILES, instance=score)
        if form.is_valid():
            form.save()
            return redirect('teacher_panel')
        return render(request, 'accounts/giving_score.html', {'form': form})



def error_404_view(request, exception):
    return render(request, 'accounts/404.html')

def badType(request):
    return render(request, 'accounts/badtype.html')