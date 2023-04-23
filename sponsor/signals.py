from django.dispatch import receiver
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from fpdf import FPDF
from .models import Donation
from users.models import Buddy, StartYoungUKUser


@receiver(valid_ipn_received)
def paypal_payment_received(sender, **kwargs):
    ipn_obj = sender
            
    # check for a successful subscription payment IPN
    if ipn_obj.txn_type == "subscr_payment":
        buddy_id, user_id = int(ipn_obj.custom.split(' ')[1]), int(ipn_obj.custom.split(' ')[3])
        try:
            buddy = Buddy.objects.get(id=buddy_id)
        except Exception:
            print('Paypal ipn_obj data not valid!', ipn_obj, 'sdp_payment')
        else:
            buddy.sdp_active = True
            buddy.save()
            
    # check for a successful "regular" donation IPN
    elif ipn_obj.payment_status == ST_PP_COMPLETED:
        print('ST_PP_COMPLETED')
        try:
            donation = Donation.objects.get(pk=ipn_obj.invoice)
            # Check donation amount is as expected
            assert ipn_obj.mc_gross == donation.amount and ipn_obj.mc_currency == 'GBP'
        except Exception:
            print('Paypal ipn_obj data not valid!', ipn_obj, 'donation')
        else:
            donation.is_successful = True
            donation.save()
            sendthankyoumail(donation.email)

    # check for failed subscription payment IPN
    elif ipn_obj.txn_type == "subscr_failed":
        send_email(ipn_obj.payer_email, 'StartYoung UK Subscription Payment Failure', "email_payment_failed.html")
        print('SDP subscription payment failed', ipn_obj)

    # check for subscription cancellation IPN
    elif ipn_obj.txn_type == "subscr_cancel":
        buddy_id, user_id = int(ipn_obj.custom.split(' ')[1]), int(ipn_obj.custom.split(' ')[3])
        try:
            buddy = Buddy.objects.get(id=buddy_id)
            user = StartYoungUKUser.objects.get(user=user_id)
        except Exception:
            print('Paypal ipn_obj data not valid!', ipn_obj, 'subscr_cancel')
        else:
            buddy.sdp_active = False
            user.is_buddy = False
            buddy.save()
            user.save()
            
            send_email(ipn_obj.payer_email, 'StartYoung UK Subscription Cancellation', "email_subscription_cancelled.html")
            print('SDP subscription cancelled', ipn_obj)
    
    else:
        print('Paypal payment status: %s. Paypal transaction type: %s' % (ipn_obj.payment_status, ipn_obj.txn_type))



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
    
def send_email(email, subject, template_name):
    body = render_to_string('email/' + template_name)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    email = EmailMessage(subject, body, email_from, recipient_list)
    email.content_subtype = "html"
    email.send()