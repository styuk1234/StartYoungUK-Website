from django.shortcuts import render,redirect
from .forms import DonationForm
from django.contrib import messages
from sponsor.models import Donations
from django.conf import settings
from django.core.mail import send_mail

def sponsor(request):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,f'Thank you for your donation!')
            sendthankyoumail(form.cleaned_data['email_id'])
        else:
            print('invalid')
            messages.error(request, 'Invalid Form')

    form = DonationForm()    
    return render(request, 'sponsor.html', {'form':form})

def sendthankyoumail(email_id):
    subject = 'Thank you for your donation!'
    message = f'Hi, thank you for donation to StartYoungUK charity.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email_id, ]
    send_mail( subject, message, email_from, recipient_list )