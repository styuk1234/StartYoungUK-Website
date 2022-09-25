from django.shortcuts import render,redirect
from .forms import UserRegisterForm
from django.contrib import messages
from users.models import StartYoungUKUser
from django.contrib.auth.models import User
from phonenumber_field.phonenumber import PhoneNumber


# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            syuk_user = StartYoungUKUser()
            syuk_user.user = User.objects.get(email=form.cleaned_data.get('email'))
            syuk_user.display_name = form.cleaned_data.get('display_name')
            syuk_user.phone_number = form.cleaned_data.get('phone_number')
            syuk_user.email = form.cleaned_data.get('email')
            syuk_user.address = form.cleaned_data.get('address')
            syuk_user.user_type = form.cleaned_data.get('user_type')
            syuk_user.crn_no = form.cleaned_data.get('crn_no')
            syuk_user.save()
            messages.success(request,f'Account created successfully for {username}!')
            return redirect('login')
 
    else:
        form = UserRegisterForm()
        
    return render(request, 'users/register.html', {'form':form})