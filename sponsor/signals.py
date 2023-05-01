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

from io import BytesIO
from django.template.loader import get_template
from django.core.mail import EmailMessage
from xhtml2pdf import pisa


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
            elif not user.is_buddy and user.sdp_frequency != 'N':
                sendEmailFixedContent(user.email,'Your systematic donation plan has been set up', 'email_templates/sdp_success.html')
                
            
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

            #for pdf receipt
            charity = CharityDetail.objects.get(id=1)
            selected_donation = Donation.objects.get(trxn_id=donation.trxn_id)
            context = {'donation': selected_donation, 'charity': charity}
            
            template_path = 'donation_receipt.html'
            template = get_template(template_path)
            html = template.render(context)
            result = BytesIO()
            pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
            if not pdf.err:
                with open('Receipt.pdf', 'wb') as f:
                    f.write(result.getvalue())
                sendEmailFixedContent(donation.email,'Thank You for Your Donation','email_templates/donation_success.html', 'Receipt.pdf' )
            else:
                print(pdf.err)           
 

    # check for failed subscription payment IPN
    elif ipn_obj.txn_type == "subscr_failed":
        # send_email(ipn_obj.payer_email, 'StartYoung UK Subscription Payment Failure', "email_payment_failed.html")
        sendEmailFixedContent(ipn_obj.payer_email,'StartYoung UK Subscription Payment Failure', 'email_templates/sdp_failed.html')
        print('SDP subscription payment failed', ipn_obj)

    # check for subscription cancellation IPN
    elif ipn_obj.txn_type == "subscr_cancel":
        buddy_id, user_id = int(ipn_obj.custom.split(' ')[1]), int(ipn_obj.custom.split(' ')[3])
        try:
            if buddy_id != 0:
                buddy = Buddy.objects.get(id=buddy_id)
            user = StartYoungUKUser.objects.get(user=user_id)
        except Exception:
            print('Paypal ipn_obj data not valid!', ipn_obj, 'subscr_cancel')
        else:
            user.is_buddy = False
            user.sdp_amount = 0
            user.sdp_frequency = 'N'
            user.save()
            
            if buddy_id != 0:
                buddy.status = 'opted_out'
                buddy.save()            
                sendEmailFixedContent(user.email,'Thank you for being a buddy', 'email_templates/buddy_sdp_cancel.html')

                #send notification email to syuk people
                charity_email = CharityDetail.objects.get(id=1).email
                body = f'The user {user.user.first_name} {user.user.last_name} has opted out. Their email address is: {user.email}'
                email_from = settings.EMAIL_HOST_USER
                recipient = [charity_email,]
                subject = f'A buddy has opted out: {user.user.first_name} {user.user.last_name}'
                email = EmailMessage(subject, body, email_from, recipient)
                email.send()
                
            else:
                sendEmailFixedContent(user.email,'Your systematic donation plan has been cancelled', 'email_templates/sdp_cancel.html')



            print('SDP subscription cancelled', ipn_obj)
    
    else:
        print('Paypal payment status: %s. Paypal transaction type: %s' % (ipn_obj.payment_status, ipn_obj.txn_type))



# def sendthankyoumail(email):
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", size = 15)
#     pdf.cell(200, 10, txt = "Acknowlegment Receipt",
# 		ln = 1, align = 'C')
#     pdf.cell(200, 10, txt = "Thank you for your donation. Receipt No#1234",
# 		ln = 2, align = 'C')
#     pdf.output("Receipt.pdf")
#     subject = 'Thank you for your donation!'
#     message = f'Hi, thank you for donation to our charity.'
#     email_from = settings.EMAIL_HOST_USER
#     recipient_list = [email, ]
#     email = EmailMessage(
#     subject, message, email_from, recipient_list)
#     email.attach_file('Receipt.pdf')
#     email.send()

# def sendthankyoumail(email, context):
#     template_path = 'donation_receipt.html'
#     template = get_template(template_path)
#     html = template.render(context)
#     result = BytesIO()
#     pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
#     if not pdf.err:
#         with open('Receipt.pdf', 'wb') as f:
#             f.write(result.getvalue())
#         subject = 'Thank you for your donation!'
#         message = 'Hi, thank you for your donation to our charity.'
#         email_from = settings.EMAIL_HOST_USER
#         recipient_list = [email, ]
#         email = EmailMessage(subject, message, email_from, recipient_list)
#         email.attach_file('Receipt.pdf')
#         email.send()
#     else:
#         print(pdf.err)

# def send_email(email, subject, template_name):
#     body = render_to_string('email/' + template_name)
#     email_from = settings.EMAIL_HOST_USER
#     recipient_list = [email, ]
#     email = EmailMessage(subject, body, email_from, recipient_list)
#     email.content_subtype = "html"
#     email.send()