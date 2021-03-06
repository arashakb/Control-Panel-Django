from django.urls import path
from . import views
from django.conf import  settings
from django.conf.urls.static import static
from accounts.views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('teacher_panel', TeacherPanel.as_view(), name='teacher_panel'),
    path('student_panel', StudentPanel.as_view(), name='student_panel'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('exercise/<str:pk>/', ExerciseView.as_view(), name='exercise'),

    path('account/', views.accountSettings, name='account'),

    path('video/<str:pk>', VideoView.as_view(), name='video'),
    path('exercise_form/', ExerciseForm.as_view(), name='exercise_form'),
    path('submit_answer/<str:pk>', SubmitAnswer.as_view(), name='submit_answer'),
    path('giving_score/<str:pk>', GivingScore.as_view(), name='giving_score'),

    path('bad_type', views.badType, name='bad_type')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)