from django.shortcuts import render, redirect
from .forms import SDPForm, UserRegisterForm, UserLoginForm, UpdateUserForm, MentorRegistrationForm
from home.forms import CampaignForm
from home.models import Campaign
from django.contrib import messages
from users.models import StartYoungUKUser, Mentor, Child
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .decorators import user_not_authenticated
from verify_email.email_handler import send_verification_email
from verify_email.confirm import verify_user
from django.core.signing import SignatureExpired, BadSignature
from base64 import urlsafe_b64decode
from verify_email.errors import (
    InvalidToken,
)

# Create your views here.
@user_not_authenticated
def verify_user_and_activate(request,useremail, usertoken):
    try:
        verified = verify_user(useremail, usertoken)
        if verified is True:
            useremail=urlsafe_b64decode(str(useremail)).decode('UTF-8')
            syuk_user=StartYoungUKUser.objects.get(email=str(useremail))
            syuk_user.is_verified=True
            syuk_user.save()
            messages.success(request, "User has been verified")
            return redirect('login')
        else:
            raise ValueError
    except (ValueError, TypeError) as error:
        messages.warning(request, "There is something wrong with this link... Verification failed")
        return redirect('login')
    except SignatureExpired:
        messages.warning(request, "The link has lived its life. Request a new one !")
        return redirect('login')
    except BadSignature:
        messages.warning(request, "This link was modified before verification.Faulty Link Detected!")
        return redirect('login')
    except InvalidToken:
        messages.warning(request, "This link is invalid or been used already, we cannot verify using this link.")
        return redirect('login')



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
        form = UserLoginForm(data=request.POST)
        print(len(list(form.errors.items())))
        print(form.errors.items())
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
                    return redirect('login')
                
                if key == '__all__' and error[0] == 'Please enter a correct username and password. Note that both fields may be case-sensitive.':
                    try:
                        userobj=User.objects.get(username=form.cleaned_data["username"])
                        syukuser=StartYoungUKUser.objects.get(email=userobj.email)
                        if not syukuser.is_verified and not userobj.is_active:
                            messages.error(request,"Email not verified! Please check your email box")
                            return redirect('login')
                        messages.error(request,"Please enter a correct username and password. Note that both fields may be case-sensitive.")
                        return redirect('login')
                    
                    except User.DoesNotExist:
                        messages.error(request,"User does not exist ! Please create an account")
                        return redirect('login')

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
def start_campaign(request):
    if request.method=='POST':
        form = CampaignForm(request.POST)
        print("It's a POST request")
        if form.is_valid():
            print("Is Valid?")
            form.save()
            '''
            campaign_obj = Campaign()
            campaign_obj.campaign_title = form.cleaned_data.get('campaign_title')
            print(campaign_obj.title)
            campaign_obj.campaign_description = form.cleaned_data.get('campaign_description')
            campaign_obj.collection_target = form.cleaned_data.get('collection_target')
            campaign_obj.campaign_deadline = form.cleaned_data.get('campaign_deadline')
            campaign_obj.campaign_image = form.cleaned_data.get('campaign_image')
            
            campaign_obj.save()
            '''
            print("Object saved successfully!")
            messages.success(request,
                             f'Thanks for starting a campaign with us, your campaign has been posted successfully!')
            return redirect('userhome')
        else:
            for key, error in list(form.errors.items()):
                messages.error(request, f'{key}, {error}')
    else:
        form = CampaignForm()

    return render(request, 'start_campaign.html', {'form':form})

@login_required
def mentor(request):
    form = MentorRegistrationForm()
    if(request.method=='POST'):
        form = MentorRegistrationForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            bitmap=""
            hobbies=['painting','football','reading','dancing','singing','cooking','cricket','arts_and_crafts','adventure','writing']
            form_data = form.cleaned_data
            for i in range(10):
                if(form_data.get(hobbies[i])==True):
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
            mentor.occupation=form_data.get('occupation')
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
            if(childx.mentor == 0):
                recommended_child.append(childx)
    return render(request, 'mentor.html', {'form':form, 'recommended_child':recommended_child})

@login_required
def profile(request):
    current_user = request.user
    print(current_user.email)
    if request.method == 'POST':
        form = UpdateUserForm(request.POST)
        if form.is_valid():
            if User.objects.filter(email__iexact=form.cleaned_data.get('email')).exclude(current_user.email).count() > 1:
                messages.error(request, "This email address is already in use. Please supply a different email address.")
            else:
                syuk_user = StartYoungUKUser.objects.get(user=request.user)
                username = form.cleaned_data.get('username')
                syuk_user.display_name = form.cleaned_data.get('display_name')
                syuk_user.phone_number = form.cleaned_data.get('phone_number')
                syuk_user.email = form.cleaned_data.get('email')
                syuk_user.address = form.cleaned_data.get('address')
                syuk_user.save()
                userx = User.objects.get(email=form.cleaned_data['email'])
                userx.email = form.cleaned_data['email']
                userx.save()
                messages.success(request,
                                f'Account updated successfully for {username}!')
                return redirect('profile')
        else:
            for key, error in list(form.errors.items()):
                if key == 'captcha' and error[0] == 'This field is required.':
                    messages.error(request, "You must pass the reCAPTCHA test to register.")
                    continue

                messages.error(request, error)
    else:
        form = UpdateUserForm(instance=request.user.startyoungukuser)

    return render(request, 'profile.html', {'form': form})