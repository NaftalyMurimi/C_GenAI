from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "index.html")
def home(request):
    return render(request, "home.html")
def courses(request):
    return render(request, "courses.html")
def signin(request):
    return render(request, "signin.html")
def signup(request):
    return render(request, "signup.html")
def student_dashboard(request):
    return render(request, "student/student_dashboard.html")
def student_profile(request):
    return render(request, "student/student_profile.html")
def student_progress(request):
    return render(request, "student/student_progress.html")
def c_compiler(request):
    return render(request, "student/c_compiler.html")










