from django.core.mail import EmailMessage, EmailMultiAlternatives
# from fpdf import FPDF
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import os

from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import get_template
from email.mime.image import MIMEImage

from functools import lru_cache



# TODO: this needs to be updated after discussion with styuk
def sendBuddyApprovalEmail(email,status):
    subject = 'Update: StartYoungUK mentor sign up update'
    message = f'Hi, thank you signing up to be a buddy, you\'ve been ' + status
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    email = EmailMessage(
    subject, message, email_from, recipient_list)
    # email.attach_file('example_attachment.pdf')
    email.send()

# def sendLetterReminderEmail(email):
#     subject = 'Reminder: write letter to your child'
#     message = 'Hi, time to write your child a letter'
#     email_from = settings.EMAIL_HOST_USER
#     recipient_list = [email, ]
#     email = EmailMessage(
#     subject, message, email_from, recipient_list)
#     # email.attach_file('example_attachment.pdf')
#     email.send()


def sendLetterReminderEmail(email):
    html_tpl_path = 'email_templates/email_template.html'
    receiver_email = [email, ]
    subject = 'Reminder: write letter to your child'
    # Get the path to the logo image file
    logo_path = os.path.join(settings.STATIC_ROOT, 'images', 'startyounguk-logo.jpg')
    context_data =  {'image_path': logo_path}
    email_html_template = get_template(html_tpl_path).render(context_data)
    # email_msg = EmailMessage(subject, 
    #                             email_html_template, 
    #                             settings.EMAIL_HOST_USER,
    #                             receiver_email,
    #                             reply_to=[settings.EMAIL_HOST_USER]
    #                             )
    
    email_msg = EmailMultiAlternatives(
        subject=subject,
        body=email_html_template,
        from_email=settings.EMAIL_HOST_USER,
        to=receiver_email,
        reply_to=[settings.EMAIL_HOST_USER],

    )
    # with open(logo_path, 'rb') as f:
    #     image_data = f.read()
    #     email_msg.attach('startyounguk-logo.jpg', image_data, 'image/jpg')
    email_msg.content_subtype = 'html'
    email_msg.send(fail_silently=False)

    email_msg.mixed_subtype = 'related'
    email_msg.attach_alternative(email_html_template, "text/html")
    email_msg.attach(logo_data())

    email_msg.send(fail_silently=False)

@lru_cache()
def logo_data():
    logo_path = os.path.join(settings.STATIC_ROOT, 'images', 'startyounguk-logo.jpg')

    with open(logo_path, 'rb') as f:
        logo_data = f.read()
    logo = MIMEImage(logo_data)
    logo.add_header('Content-ID', '<logo>')
    return logo