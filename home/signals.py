from django.core.mail import EmailMessage
# from fpdf import FPDF
from django.conf import settings


def sendMentorApprovalEmail(email,status):
    subject = 'Update: StartYoungUK mentor sign up update'
    message = f'Hi, thank you signing up to be a buddy, you\'ve been ' 
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    email = EmailMessage(
    subject, message, email_from, recipient_list)
    email.attach_file('Receipt.pdf')
    email.send()