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
    path('student_home/', views.student_home, name='student_home'),
    # path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('activate/<uidb64>/<token>', views.activate, name = 'activate'),
    path('password_change/', views.password_change, name='password_change'),
    path('password_recovery/', views.password_recovery, name= 'password_recovery'),
    path('reset/<uidb64>/<token>', views.passwordResetConfirm, name = 'password_reset_confirm'),
    path('profile/<username>', views.profile, name='profile'),
]
