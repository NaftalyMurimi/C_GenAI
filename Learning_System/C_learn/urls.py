from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.index, name='index'),
    # path('home/', views.home, name='home'),
    path('courses/', views.courses, name='courses'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student_progress/', views.student_progress, name='student_progress'),
    path('student_profile/', views.student_profile, name='student_profile'),
    path('c_compiler/', views.c_compiler, name='c_compiler'),
]
