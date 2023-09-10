from django.shortcuts import render, redirect
from home.models import Opportunity
from datetime import date
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse


def contact(request):
    opportunities = Opportunity.objects.all()
    if request.method == 'POST':
        name = request.POST.get('Name')
        email = request.POST.get('Email')
        subject = request.POST.get('Subject')
        message = request.POST.get('Message')

        # Format the email body with sender's information
        email_body = f"Name: {name}\nEmail: {email}\nSubject: {subject}\nMessage: {message}"

        # Send the email
        send_mail(
            f"New Contact Form Submission: {subject}",
            email_body,
            settings.DEFAULT_FROM_EMAIL,
            ['startyounguk21@gmail.com'],
            fail_silently=False,
        )

        response_data = {'message': 'Message sent successfully!', 'status': 'success'}
        return JsonResponse(response_data)

    return render(
        request, "contact.html", {"opportunities": opportunities, "today": date.today(),} #"GSHEETS_CONTACT_US": settings.GSHEETS_CONTACT_US}
    )
