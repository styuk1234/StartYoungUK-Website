from django.core.mail import EmailMessage
# from fpdf import FPDF
from django.conf import settings

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

def sendLetterReminderEmail(email):
    subject = 'Reminder: write letter to your child'
    message = 'Hi, time to write your child a letter'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    email = EmailMessage(
    subject, message, email_from, recipient_list)
    # email.attach_file('example_attachment.pdf')
    email.send()