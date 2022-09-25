from django.shortcuts import render,redirect
from .forms import DonationForm
from django.contrib import messages
from sponsor.models import Donations
from django.contrib.auth.models import User

def sponsor(request):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,f'Thank you for your donation!')
        else:
            print('invalid')
            messages.error(request, 'Invalid Form')

    form = DonationForm()    
    return render(request, 'sponsor.html', {'form':form})