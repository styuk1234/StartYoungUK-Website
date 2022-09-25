from django.shortcuts import render,redirect
from .forms import UserRegisterForm, UserLoginForm
from django.contrib import messages
from users.models import StartYoungUKUser
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .decorators import user_not_authenticated
from verify_email.email_handler import send_verification_email

# Create your views here.

@user_not_authenticated
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            syuk_user = StartYoungUKUser()
            syuk_user.user = User.objects.get(email=form.cleaned_data['email'])
            syuk_user.display_name = form.cleaned_data.get('display_name')
            syuk_user.phone_number = form.cleaned_data.get('phone_number')
            syuk_user.email = form.cleaned_data.get('email')
            syuk_user.address = form.cleaned_data.get('address')
            syuk_user.user_type = form.cleaned_data.get('user_type')
            syuk_user.crn_no = form.cleaned_data.get('crn_no')
            syuk_user.save()
            messages.success(request,f'Account created successfully for {username}! Check email to complete verification.')
            inactive_user = send_verification_email(request, form)
            return redirect('login')
        else:
            for key, error in list(form.errors.items()):
                if key == 'captcha' and error[0] == 'This field is required.':
                    messages.error(request, "You must pass the reCAPTCHA test to register.")
                    continue
                
                messages.error(request, error) 
    else:
        form = UserRegisterForm()
        
    return render(request, 'users/register.html', {'form':form})

@user_not_authenticated
def captcha_login(request):
    if request.method == "POST":
        form = UserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                return redirect("home")

        else:
            for key, error in list(form.errors.items()):
                if key == 'captcha' and error[0] == 'This field is required.':
                    messages.error(request, "You must pass the reCAPTCHA test to login.")
                    continue
   
                messages.error(request, error) 
    else:
        form = UserLoginForm()

    return render(
        request=request,
        template_name="users/login.html",
        context={"form": form}
        )

@login_required
def captcha_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully!")
    return redirect("login")