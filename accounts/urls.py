from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('teacher_panel', views.teacherPanel, name='teacher_panel'),
    path('student_panel', views.studentPanel, name='student_panel'),
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout')
]