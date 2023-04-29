from django.shortcuts import render, redirect
from .forms import SDPForm, UserRegisterForm, UserLoginForm, UpdateUserForm, BuddyRegistrationForm, UserEmailPasswordResetForm
from home.forms import CampaignForm
from home.models import Campaign
from django.contrib import messages
from users.models import StartYoungUKUser, Buddy
from sponsor.models import Donation
from home.models import Campaign
from about.models import CharityDetail
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .decorators import user_not_authenticated
from verify_email.email_handler import send_verification_email
from verify_email.confirm import verify_user
from django.core.signing import SignatureExpired, BadSignature
from base64 import urlsafe_b64decode
import os
from decouple import config
from paypal.standard.forms import PayPalPaymentsForm
from django.urls import reverse
from django.views.generic import TemplateView
from verify_email.errors import (
    InvalidToken,
)


#for pdf generation
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.shortcuts import render
from django.http import HttpResponse
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa

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
        print(form.is_valid())
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
                             f'Account created successfully for {username}! Check email to complete your verification and access the website.')
            inactive_user = send_verification_email(request, form)
            return redirect('login')
        else:
            for key, error in list(form.errors.items()):
                if key == 'captcha' and error[0] == 'This field is required.':
                    messages.error(request, "You must pass the reCAPTCHA test to register.")
                    continue

                messages.error(request, error)
            return redirect('register')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


@user_not_authenticated
def captcha_login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
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
                    return redirect('login')
                
                if key == '__all__' and error[0] == 'Please enter a correct username and password. Note that both fields may be case-sensitive.':
                    try:
                        userobj=User.objects.get(username=form.cleaned_data["username"])
                        syukuser=StartYoungUKUser.objects.get(email=userobj.email)
                        if not syukuser.is_verified and not userobj.is_active:
                            messages.error(request,"This email address is not verified! Please check your inbox and verify from there to access the content.")
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

@user_not_authenticated
def password_email_reset(request):
    if request.method == "POST":
        form = UserEmailPasswordResetForm(data=request.POST)

    return render(
        request=request,
        template_name="users/password_reset.html",
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
def sdp(request):
    form=SDPForm()
    
    paypal_dict = {
        "cmd": "_xclick-subscriptions",
        "src": "1", # make payments recur
        "sra": "1", # reattempt payment on payment error
        "no_note": "1", # remove extra notes
        "item_name": "SYUK systematic donation",
        "business": config('PAYPAL_BUSINESS_ACCOUNT'),
        'currency_code': 'GBP',
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('sdp-return')),
        "cancel_return": request.build_absolute_uri(reverse('sdp-cancel'))
    }
    
    user_id = request.user.startyoungukuser.user.id
    
    if request.user.startyoungukuser.sdp_frequency == 'W':
        sdp_frequency = 'Weekly'
    elif request.user.startyoungukuser.sdp_frequency == 'F':
        sdp_frequency = 'Forthnightly'
    elif request.user.startyoungukuser.sdp_frequency == 'M':
        sdp_frequency = 'Monthly'
    else:
        sdp_frequency = 'N'
    sdp_amount = request.user.startyoungukuser.sdp_amount
    
    if request.user.startyoungukuser.is_buddy:
        # User is a Buddy: prepopulate SDP amount and frequency fields
        buddy_id = Buddy.objects.get(user=request.user.startyoungukuser.user).id
        paypal_dict["a3"] = 5 # amount
        paypal_dict["p3"] = 1 # duration of each unit
        paypal_dict["t3"] = 'W' # duration unit ("W for Weekly")
        paypal_dict["custom"] = "buddy_id %s user_id %s %s %s" % (buddy_id, user_id, 1, 'W')
        
    else:
        # User is not a Buddy: let them choose SDP amount and frequency fields
        paypal_dict["a3"] = form['amount'].value() # amount
        if form['frequency'].value() == 'W':
            paypal_dict["p3"] = 1
            paypal_dict["t3"] = 'W' # Weekly
            paypal_dict["custom"] = "buddy_id %s user_id %s %s %s" % (0, user_id, 1, 'W')
        elif form['frequency'].value() == 'F':
            paypal_dict["p3"] = 14
            paypal_dict["t3"] = 'D' # Fortnightly
            paypal_dict["custom"] = "buddy_id %s user_id %s %s %s" % (0, user_id, 14, 'D')
        elif form['frequency'].value() == 'M':
            paypal_dict["p3"] = 1
            paypal_dict["t3"] = 'M' # Monthly
            paypal_dict["custom"] = "buddy_id %s user_id %s %s %s" % (0, user_id, 1, 'M')
        else:
            print('invalid SDP choice')
            # raise Exception

    paypal_btn = PayPalPaymentsForm(initial=paypal_dict, button_type="subscribe")

    if request.method=='POST':
        form = SDPForm(request.POST)
        if form.is_valid():
            print('form valid')
            
    return render(request, 'sdp.html', {'form':form, 'paypal_btn': paypal_btn, 'is_buddy': request.user.startyoungukuser.is_buddy, 'sdp_frequency': sdp_frequency, 'sdp_amount': sdp_amount})


class PaypalReturnView(TemplateView):
    template_name = 'paypal_success.html'

class PaypalCancelView(TemplateView):
    template_name = 'paypal_cancel.html'


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
def buddy(request):
    form = BuddyRegistrationForm()
    if(request.method=='POST'):
        form = BuddyRegistrationForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            # bitmap=""
            # hobbies=['painting','football','reading','dancing','singing','cooking','cricket','arts_and_crafts','adventure','writing']
            form_data = form.cleaned_data
            # for i in range(10):
            #     if(form_data.get(hobbies[i])==True):
            #         bitmap+="1"
            #     else:
            #         bitmap+="0"

            try:
                buddy = Buddy.objects.get(user=request.user)
            except Buddy.DoesNotExist:
                buddy = Buddy()
            # buddy.hobbies=bitmap   
            # buddy.occupation=form_data.get('occupation')
            buddy.description = form_data.get('description')
            buddy.user=User.objects.get(username=request.user.username)
            buddy.status = 'pending'
            buddy.save()
            # TODO: this message is hard notice. instead, if they are approved, or pending they should be taken to a different page to show their current status
            # messages.success(request,f'Buddy request has been sent and is pending approval. You will receive an email once your application is approved')
            
    # best_match_score=[0,0,0]
    # best_match_child=[-1,-1,-1]
    # for child in Child.objects.all():
    #     scr=bin(int(child.hobbies,2) & int(request.user.buddy.hobbies,2)).count("1")
    #     if scr>best_match_score[0]:
    #         best_match_score[0]=scr
    #         best_match_child[0]=child.child_id
    #     elif scr> best_match_score[1]:
    #         best_match_score[1]=scr
    #         best_match_child[1]=child.child_id
    #     elif scr> best_match_score[2]:
    #         best_match_score[2]=scr
    #         best_match_child[2]=child.child_id
    # recommended_child=[]
    # for x in best_match_child:
    #     if(x != -1):
    #         childx=Child.objects.get(child_id=x)
    #         if(childx.mentor == 0):
    #             recommended_child.append(childx)
    return render(request, 'mentor.html', {'form':form})

@login_required
def profile(request):
    current_user = request.user
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, request.FILES,instance=current_user,user=request.user.startyoungukuser)
        if form.is_valid():
            if User.objects.filter(email__iexact=form.cleaned_data.get('email')).count() > 1:
                messages.error(request, "This email address is already in use. Please supply a different email address.")
            else:
                syuk_user = StartYoungUKUser.objects.get(user=request.user)
                # username = form.cleaned_data.get('username')
                syuk_user.display_name = form.cleaned_data.get('display_name')
                syuk_user.phone_number = form.cleaned_data.get('phone_number')
                syuk_user.email = form.cleaned_data.get('email')
                syuk_user.address = form.cleaned_data.get('address')
                if len(request.FILES) !=0:
                    if form.cleaned_data['image'] and os.path.exists(syuk_user.image.path):
                        os.remove(syuk_user.image.path)
                    syuk_user.image = form.cleaned_data.get('image')
                syuk_user.save()
                userx = User.objects.get(email=form.cleaned_data['email'])
                userx.email = form.cleaned_data['email']
                userx.save()
                messages.success(request,
                                f'Account updated successfully for {request.user}!')
                return redirect('profile')
        else:
            for key, error in list(form.errors.items()):
                if key == 'captcha' and error[0] == 'This field is required.':
                    messages.error(request, "You must pass the reCAPTCHA test to register.")
                    continue

                messages.error(request, error)
            return redirect('profile')
    else:
        form = UpdateUserForm(user=request.user.startyoungukuser,instance=request.user.startyoungukuser)
    return render(request, 'profile.html', {'form': form})


@login_required
def past_donations(request):
    user_id = request.user.id
    donations = Donation.objects.filter(user_id=user_id, is_successful=True)
    charity = CharityDetail.objects.get(id=1)
    campaign_names = []
    for donation in donations:
        if donation.campaign_id != 0:
            campaign = Campaign.objects.get(pk=donation.campaign_id)
            campaign_names.append(campaign.campaign_title)
        else:
            campaign_names.append("Standard Donation")
    donation_zip = zip(donations, campaign_names)

    if request.method == 'POST':
        selected_donation_id = request.POST.getlist('chosen-donation')
        selected_donation = Donation.objects.get(trxn_id__in=selected_donation_id)
        donation_date = selected_donation.date_donation.strftime("%Y-%m-%d %H:%M:%S")
        template_path = 'donation_receipt.html'
        context = {'donation': selected_donation, 'charity': charity}

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="receipt_{donation.name}_{donation_date}.pdf"'
        buffer = BytesIO()
        template = get_template(template_path)
        html = template.render(context)
        pisa_status = pisa.CreatePDF(html, dest=response, encoding='utf-8')
        if pisa_status.err:
            return HttpResponse('Error rendering PDF', status=400)
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response

    return render(request, 'past_donations.html',{'donation_zip': donation_zip})

def donation_pdf_receipt(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)

    # get checked donations
    checked_donations = request.POST.getlist('chosen-donation')
    user_id = request.user.id
    user_name = str(request.user.first_name) +" "+ str(request.user.last_name)
    donations = Donation.objects.filter(user_id=user_id,trxn_id__in=checked_donations)

    lines = ['Donor name: '+ user_name]
    donation_date = None
    for donation in donations:
        lines.append(" ")
        if donation.campaign_id != 0:
            campaign = Campaign.objects.get(pk=donation.campaign_id)
            lines.append('Campaign Name: ' + campaign.campaign_title)
        else:
            lines.append('Campaign Name: Standard Donation')
        lines.append('Amount: £' + str(donation.amount))
        donation_date = donation.date_donation.strftime("%Y-%m-%d %H:%M:%S")
        lines.append('Date: ' + donation_date)

    for line in lines:
        textob.textLine(line)

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    filename = f"donation_{user_name}_{donation_date}.pdf"
    return FileResponse(buf, as_attachment=True, filename=filename)