from django.core.mail import EmailMessage, EmailMultiAlternatives
# from fpdf import FPDF
from django.conf import settings
import os
from django.template.loader import get_template
from email.mime.image import MIMEImage
from functools import lru_cache
from .models import EmailContent


# def sendBuddyApprovalEmail(email,status):
#     subject = 'Update: StartYoungUK mentor sign up update'
#     message = f'Hi, thank you signing up to be a buddy, you\'ve been ' + status
#     email_from = settings.EMAIL_HOST_USER
#     recipient_list = [email, ]
#     email = EmailMessage(
#     subject, message, email_from, recipient_list)
#     # email.attach_file('example_attachment.pdf')
#     email.send()


def sendEmail(email):
    html_tpl_path = 'email_templates/email_template.html'
    receiver_email = [email, ]
    subject = 'Reminder: write letter to your child'
    # Get the path to the logo image file
    logo_path = os.path.join(settings.STATIC_ROOT, 'images', 'startyounguk-logo.jpg')
    context_data =  {'image_path': logo_path}
    email_html_template = get_template(html_tpl_path).render(context_data)

    email_msg = EmailMultiAlternatives(
        subject=subject,
        body=email_html_template,
        from_email=settings.EMAIL_HOST_USER,
        to=receiver_email,
        reply_to=[settings.EMAIL_HOST_USER],

    )

    # move this: pdf attachments
    email_content = EmailContent.objects.get(email_type='Letter')

    email_msg.content_subtype = 'html'
    email_msg.send(fail_silently=False)

    email_msg.mixed_subtype = 'related'
    email_msg.attach_alternative(email_html_template, "text/html")
    email_msg.attach(logo_data())
    email_msg.attach(email_content.attachment.name, email_content.attachment.read())

    email_msg.send(fail_silently=False)

@lru_cache()
def logo_data():
    logo_path = os.path.join(settings.STATIC_ROOT, 'images', 'startyounguk-logo.jpg')

    with open(logo_path, 'rb') as f:
        logo_data = f.read()
    logo = MIMEImage(logo_data)
    logo.add_header('Content-ID', '<logo>')
    return logo