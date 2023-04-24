from django.core.mail import EmailMessage, EmailMultiAlternatives
# from fpdf import FPDF
from django.conf import settings
import os
from django.template.loader import get_template
from email.mime.image import MIMEImage
from functools import lru_cache
from .models import EmailContent

def sendEmail(email, email_type):
    html_tpl_path = 'email_templates/email_template.html'
    receiver_email = [email, ]
    email_content = EmailContent.objects.get(email_type=email_type)
    subject = email_content.subject
    # Get the path to the logo image file
    logo_path = os.path.join(settings.STATIC_ROOT, 'images', 'startyounguk-logo.jpg')

    context_data =  {'image_path': logo_path, 'header':email_content.header,'body':email_content.body,'signature':email_content.signature, 'type': email_content.email_type }

    email_html_template = get_template(html_tpl_path).render(context_data)

    email_msg = EmailMultiAlternatives(
        subject=subject,
        body=email_html_template,
        from_email=settings.EMAIL_HOST_USER,
        to=receiver_email,
        reply_to=[settings.EMAIL_HOST_USER],
    )

    email_msg.content_subtype = 'html'

    email_msg.mixed_subtype = 'related'
    email_msg.attach_alternative(email_html_template, "text/html")
    email_msg.attach(logo_data())

    if email_content.attachment:
        email_msg.attach(email_content.attachment.name, email_content.attachment.read())
    if email_content.attachment2:
        email_msg.attach(email_content.attachment2.name, email_content.attachment2.read())
    if email_content.attachment3:
        email_msg.attach(email_content.attachment3.name, email_content.attachment3.read())
    if email_content.attachment4:
        email_msg.attach(email_content.attachment4.name, email_content.attachment4.read())
    if email_content.attachment5:
        email_msg.attach(email_content.attachment5.name, email_content.attachment5.read())

    email_msg.send(fail_silently=False)

@lru_cache()
def logo_data():
    logo_path = os.path.join(settings.STATIC_ROOT, 'images', 'startyounguk-logo.jpg')

    with open(logo_path, 'rb') as f:
        logo_data = f.read()
    logo = MIMEImage(logo_data)
    logo.add_header('Content-ID', '<logo>')
    return logo