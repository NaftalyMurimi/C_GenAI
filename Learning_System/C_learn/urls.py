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
    path('c_compiler/', views.c_compiler, name='c_compiler'),
  
    path('student_profile/', views.student_profile, name='student_profile'),
    path('student_home/', views.student_home, name='student_home'),
    # path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('activate/<uidb64>/<token>', views.activate, name = 'activate'),
    path('student_change_password/', views.student_change_password, name='student_change_password'),
    path('student_password_recovery/', views.student_password_recovery, name= 'student_password_recovery'),
    path('reset/<uidb64>/<token>', views.passwordResetConfirm, name = 'password_reset_confirm'),
    # path('student_profile_update/<username>', views.student_profile_update, name='student_profile_update'),
]
