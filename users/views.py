from asyncio.windows_events import NULL
from django.shortcuts import render, redirect
from .forms import SDPForm, UserRegisterForm, UserLoginForm, UpdateUserForm, MentorRegistrationForm
from django.contrib import messages
from users.models import StartYoungUKUser, Mentor, Child
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
            messages.success(request,
                             f'Account created successfully for {username}! Check email to complete verification.')
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

    return render(request, 'users/register.html', {'form': form})


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
                return redirect("userhome")

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


@login_required
def userhome(request):
    return render(request, 'userhome.html')


@login_required
def profile(request):
    return render(request, 'profile.html')


# def donate_money(request):
#     return redirect('donate')

# def donate_kind(request):
#     return redirect('donate')

@login_required
def sdp(request):
    form=SDPForm()
    if request.method=='POST':
        form = SDPForm(request.POST)
        if form.is_valid():
            messages.success(request,
                             f'You have successfully subscribed to Systematic Donatino Plan.')
    return render(request, 'sdp.html', {'form':form})


@login_required
def mentor(request):
    form = MentorRegistrationForm()
    if(request.method=='POST'):
        form = MentorRegistrationForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            bitmap=""
            hobbies=['painting','football','reading','dancing','singing','cooking','cricket','arts_and_crafts','adventure','writing']
            form = form.cleaned_data
            for i in range(10):
                if(form.get(hobbies[i])==True):
                    bitmap+="1"
                else:
                    bitmap+="0"
            # print(request.user.username)
            # print(User.objects.get(username=request.user.username))
            # mentor.name=StartYoungUKUser.display_name
            try:
                mentor = Mentor.objects.get(user=request.user)
            except Mentor.DoesNotExist:
                mentor = Mentor()
            mentor.hobbies=bitmap   
            mentor.occupation=form.get('occupation')
            mentor.user=User.objects.get(username=request.user.username)
            mentor.save()
            messages.success(request,f'Mentor profile updated successfully! Please see recommended child profiles.')
    best_match_score=[0,0,0]
    best_match_child=[-1,-1,-1]
    for child in Child.objects.all():
        scr=bin(int(child.hobbies,2) & int(request.user.mentor.hobbies,2)).count("1")
        if scr>best_match_score[0]:
            best_match_score[0]=scr
            best_match_child[0]=child.child_id
        elif scr> best_match_score[1]:
            best_match_score[1]=scr
            best_match_child[1]=child.child_id
        elif scr> best_match_score[2]:
            best_match_score[2]=scr
            best_match_child[2]=child.child_id
    recommended_child=[]
    for x in best_match_child:
        if(x != -1):
            childx=Child.objects.get(child_id=x)
            if(childx.mentor==NULL):
                recommended_child.append(childx)
    return render(request, 'mentor.html', {'form':form, 'recommended_child':recommended_child})


def count(request):
    cnt_buddy = len(Mentor.objects.all())
    cnt_child = len(Child.objects.all())
    return render(request, 'home.html', {'cnt_buddy': cnt_buddy, 'cnt_child': cnt_child})


@login_required
def profile(request):
    current_user = request.user
    print(current_user.email)
    if request.method == 'POST':
        form = UpdateUserForm(request.POST)
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
            messages.success(request,
                             f'Account created successfully for {username}! Check email to complete verification.')
            inactive_user = send_verification_email(request, form)
            return redirect('login')
        else:
            for key, error in list(form.errors.items()):
                if key == 'captcha' and error[0] == 'This field is required.':
                    messages.error(request, "You must pass the reCAPTCHA test to register.")
                    continue

                messages.error(request, error)
    else:
        form = UpdateUserForm(instance=request.user)

    return render(request, 'profile.html', {'form': form})
