from django.shortcuts import render,redirect
from django.urls import reverse
from django.views.generic import TemplateView
from decouple import config
from paypal.standard.forms import PayPalPaymentsForm
from .forms import DonationForm
from django.contrib import messages
from .models import Donation
import uuid

def sponsor(request):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        
        # Paypal Button instance
        paypal_dict = {
            "business": config('PAYPAL_BUSINESS_ACCOUNT'),
            'currency_code': 'GBP',
            "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
            "return": request.build_absolute_uri(reverse('paypal-return')),
            "cancel_return": request.build_absolute_uri(reverse('paypal-cancel'))
        }
        
        if not request.user.is_authenticated and int(form['amount'].value()) > 40:
            messages.error(request, 'We are not able to accept donations of more than £40 from unathenticated users. Please sign in to donate a larger amount!')
        
        elif form.has_error('captcha'):
            messages.error(request, 'Please solve the Captcha before you click "Donate"')
        
        elif form.is_valid():
            donation = form.save(commit=False)
            donation.user_id = request.user.id if request.user.is_authenticated else 0
            donation.trxn_id = uuid.uuid4()
            form_data = DonationForm(instance=donation)
            
            paypal_dict['amount'] = donation.amount
            paypal_dict['invoice'] = donation.trxn_id
            paypal_btn = PayPalPaymentsForm(initial=paypal_dict)
            button_enable=True
            messages.success(request,"Please find the Paypal button below to complete the Donation!")
            donation.save()
            return render(request, 'sponsor.html', {'paypal_btn': paypal_btn,'form':form_data,'button_enable':button_enable})
        
        else:
            messages.error(request, 'There was an error with your donation. Please try again!')

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

    return render(request, 'sponsor.html', {'form': form})
        
class PaypalReturnView(TemplateView):
    template_name = 'paypal_success.html'

class PaypalCancelView(TemplateView):
    template_name = 'paypal_cancel.html'