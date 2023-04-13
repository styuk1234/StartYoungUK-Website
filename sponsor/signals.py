from django.dispatch import receiver
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.conf import settings
from django.core.mail import EmailMessage
from fpdf import FPDF
from .models import Donation
from users.models import Buddy


@receiver(valid_ipn_received)
def paypal_payment_received(sender, **kwargs):
    ipn_obj = sender
    
    # Regular donations
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        try:
            donation = Donation.objects.get(pk=ipn_obj.invoice)
            # Check donation amount is as expected
            assert ipn_obj.mc_gross == donation.amount and ipn_obj.mc_currency == 'GBP'
        except Exception:
            print('Paypal ipn_obj data not valid!')
        else:
            donation.is_successful = True
            donation.save()
            sendthankyoumail(donation.email)
            
    # Check Systematic Donation Plan
    if ipn_obj.txn_type == "subscr_payment":
        try:
            buddy = Buddy.objects.get(user=ipn_obj.user)
        except Exception:
            print('Paypal ipn_obj data not valid!')
        else:
            buddy.sdp_active = True
            buddy.save()

    # check for failed subscription payment IPN
    elif ipn_obj.txn_type == "subscr_failed":
        print('subscription failed')

    # check for subscription cancellation IPN
    elif ipn_obj.txn_type == "subscr_cancel":
        print('subscription cancelled')
    
    else:
        print('Paypal payment status not completed: %s' % ipn_obj.payment_status)



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