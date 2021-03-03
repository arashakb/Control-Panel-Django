from django.urls import path
from . import views
from django.conf import  settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('teacher_panel', views.teacherPanel, name='teacher_panel'),
    path('student_panel', views.studentPanel, name='student_panel'),
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('exercise/<str:pk>/', views.exercise, name='exercise'),
    path('account/', views.accountSettings, name='account'),
    path('video/<str:pk>', views.video, name='video'),
    path('exercise_form/', views.exerciseForm, name='exercise_form'),
    path('submit_answer/<str:pk>', views.submitAnswer, name='submit_answer')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)