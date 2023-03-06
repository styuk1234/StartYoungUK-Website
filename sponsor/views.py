from django.shortcuts import render,redirect
from .forms import DonationForm
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from fpdf import FPDF
from .models import Donation

def sponsor(request):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,f'Thank you for your donation!')
            sendthankyoumail(form.cleaned_data['email'])
        else:
            print('invalid')
            messages.error(request, 'Invalid Form')
            
    # Pre-populate user info if user is authenticated 
    if request.user.is_authenticated:
      donate=Donation()
      donate.campaign_id=0
      donate.user_id=request.user.startyoungukuser.user_id
      donate.name=request.user.startyoungukuser.display_name
      donate.email=request.user.startyoungukuser.email
      donate.mobile_number=request.user.startyoungukuser.phone_number
      form = DonationForm(instance=donate) 
    else:
      form = DonationForm()
    #cnt_sponsor = len(User.objects.all())
    return render(request, 'sponsor.html', {'form':form})

def sendthankyoumail(email):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size = 15)
    pdf.cell(200, 10, txt = "Acknowlegment Receipt",
		ln = 1, align = 'C')
    pdf.cell(200, 10, txt = "Thank you for your donation. Receipt No#1234",
		ln = 2, align = 'C')
    pdf.output("Receipt.pdf")
    subject = 'Thank you for your donation!'
    message = f'Hi, thank you for donation to our charity.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    email = EmailMessage(
    subject, message, email_from, recipient_list)
    email.attach_file('Receipt.pdf')
    email.send()