from django.dispatch import receiver
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from fpdf import FPDF
from .models import Donation
from users.models import Buddy, StartYoungUKUser
from home.signals import sendEmail, sendEmailFixedContent
from about.models import CharityDetail



@receiver(valid_ipn_received)
def paypal_payment_received(sender, **kwargs):
    ipn_obj = sender
            
    # check for a successful subscription payment IPN
    if ipn_obj.txn_type == "subscr_payment":
        
        user_id = int(ipn_obj.custom.split(' ')[3])
        duration = int(ipn_obj.custom.split(' ')[4])
        duration_unit = ipn_obj.custom.split(' ')[5]

        try:
            user = StartYoungUKUser.objects.get(user=user_id)
        except Exception:
            print('Paypal ipn_obj data not valid!', ipn_obj, 'sdp_payment')
        else:
            user.sdp_amount = ipn_obj.mc_gross
            if duration == 1 and duration_unit == 'W': # Weekly
                user.sdp_frequency = 'W'
            elif duration == 14 and duration_unit == 'D': # Fortnightly
                user.sdp_frequency = 'F'
            elif duration == 1 and duration_unit == 'M': # Monthly
                user.sdp_frequency = 'M'
            else:
                user.sdp_frequency = 'N'
            user.save()

            if user.is_buddy and user.sdp_frequency != 'N':
                sendEmail(user.email,'final')
                



        
            
    # check for a successful "regular" donation IPN
    elif ipn_obj.payment_status == ST_PP_COMPLETED:
        try:
            donation = Donation.objects.get(pk=ipn_obj.invoice)
            # Check donation amount is as expected
            assert ipn_obj.mc_gross == donation.amount and ipn_obj.mc_currency == 'GBP'
        except Exception:
            print('Regular Donation: Paypal ipn_obj data not valid!', ipn_obj)
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
            buddy.status = 'opted_out'
            user.is_buddy = False
            user.sdp_amount = 0
            user.sdp_frequency = 'N'
            buddy.save()
            user.save()
            
            sendEmailFixedContent(user.email,'Thank you for being a buddy', 'email_templates/buddy_sdp_cancel.html')
            charity_email = CharityDetail.objects.get(id=1).email
            
            #send notification email to syuk people
            body = f'The user {user.user.first_name} {user.user.last_name} has opted out. Their email address is: {user.email}'
            email_from = settings.EMAIL_HOST_USER
            recipient = [charity_email,]
            subject = f'A buddy has opted out: {user.user.first_name} {user.user.last_name}'
            email = EmailMessage(subject, body, email_from, recipient)
            email.send()

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