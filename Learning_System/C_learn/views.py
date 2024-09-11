from django.shortcuts import render



from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model, login
from django.contrib import messages
from .forms import UserRegistrationForm
from .forms import UserUpdateForm

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.http import HttpResponse

from .decorators import user_not_authenticated
from .forms import UserLoginForm
from .forms import SetPasswordForm, PasswordResetForm
from django.contrib.auth.forms import PasswordChangeForm   
from django.db.models.query_utils import Q


# libraries for email auethentication

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str 
from django.core.mail import EmailMessage
from .tokens import account_activation_token

#function to use for emails
def activateEmail(request, user, to_email):
    mail_subject = 'Activate your user account'
    message = render_to_string('template_activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to = [to_email])
    if email.send():
        messages.success(request, f"Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.")
    else:
        messages.error(request, f'Problem sending confirmation to <b>{to_email}</b>!! kindly check if the email is correct')



#function for directing the user after clickung the confirm registration link
def activate(request, uidb64, token):
    user = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = user.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active= True
        user.save()

        messages.success(request, 'Thank you for confirming your account. Now you can login')
        return redirect('signin')
    else:
        messages.error(request, 'Activation Link is Invalid')
    return redirect('signin')

@user_not_authenticated
def signup(request):  
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
                
            return redirect('signup')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = UserRegistrationForm()
    return render(
        request = request,
        template_name= 'signup.html',
        context= {'form': form}
    )


#create logout and login functions
@user_not_authenticated
def signin(request):
    # Redirect if the user is already authenticated
    if request.user.is_authenticated:
        return redirect('student_home')

    if request.method == 'POST':
        form = UserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                # If user exists and credentials are valid
                login(request, user)
                messages.success(request, f'Hello <b>{user.username}</b>, you have been logged in successfully.')
                return redirect('student_home')
            # else:
            #     # If the authentication fails, display the message
            #     messages.error(request, 'Incorrect username or password. Please try again.')
        else:
            # If form is invalid, display form errors
            # for key, error in form.errors.items():
            #     messages.error(request, f'{error}')
            messages.error(request, 'Incorrect username or password. Please try again.')

    else:
        form = UserLoginForm()

    return render(request, 'signin.html', {'form': form})



def custom_logout(request):
    logout(request)
    messages.info(request, 'Logged out successfully')
    return redirect('signin')


@login_required
def student_change_password(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed")
            return redirect('signin')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = SetPasswordForm(user)
    return render(request, 'student/student_change_password.html', {'form': form})

@user_not_authenticated
def student_password_recovery(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = "Password Reset request"
                message = render_to_string("template_reset_password.html", {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    "protocol": 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(subject, message, to=[associated_user.email])
                if email.send():
                    messages.success(request,
                        """
                        
                        <p style="text-align: center; color: #34e906;">
                            We've emailed you instructions for setting your password, if an account exists with the email you entered. 
                            You should receive them shortly.<br>If you don't receive an email, please make sure you've entered the address 
                            you registered with, and check your spam folder.
                        </p>
                        """
                    )
                else:
                    messages.error(request, "Problem sending reset password email, <b>SERVER PROBLEM</b>")

            return redirect('signin')

        for key, error in list(form.errors.items()):
            # if key == 'captcha' and error[0] == 'This field is required.':
            #     messages.error(request, "You must pass the reCAPTCHA test")
                continue

    form = PasswordResetForm()
    return render(
        request=request, 
        template_name="student/student_password_recovery.html", 
        context={"form": form}
        )
def passwordResetConfirm(request, uidb64, token):
    user = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = user.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'You password has been set Successfuly, Continue to LOGIN')
                return redirect('signin')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
        form = SetPasswordForm(user)
        return render(request, 'student/student_change_password.html', {'form': form})
    else:
        messages.error('Link has Expired')
    messages.error(request, 'Something went Wrong, Redirectint you to the homepage')
    return redirect('index')





# def student_profile_update(request, username):
#     if request.method == 'POST':
#         pass
#     user = get_user_model().objects.filter(username=username).first()
#     if user:
#         form = UserUpdateForm(instance=user)
#         return render(request, 'student_profile_update.html', context={'form':form})
#     return redirect('student_home')


def student_home(request):
    if request.user.is_authenticated:
        return render(request, 'student/student_home.html')
    else:
        return redirect('signins')


def student_dashboard(request):
    if request.user.is_authenticated:
        return render(request,'student/student_dashboard.html')
    else:
        return redirect('signin')
    # return render(request, "student/.html")

# def student_change_password(request):
#     return render(request, "student/student_change_password.html")


























# Create your views here.
def index(request):
    return render(request, "index.html")
def home(request):
    return render(request, "home.html")
def courses(request):
    return render(request, "courses.html")
# def signin(request):
#     return render(request, "signin.html")
# def signup(request):
#     return render(request, "signup.html")

def student_profile(request):
    return render(request, "student/student_profile.html")
def student_progress(request):
    return render(request, "student/student_progress.html")
def c_compiler(request):
    return render(request, "student/c_compiler.html")
