from django.shortcuts import render, redirect
from home.models import Opportunity
from datetime import date
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from rest_framework import status
from about.models import CharityDetail


def contact(request):
    opportunities = Opportunity.objects.all()
    if request.method == 'POST':
        name = request.POST.get('Name')
        email = request.POST.get('Email')
        subject = request.POST.get('Subject')
        message = request.POST.get('Message')

        # Format the email body with sender's information
        email_body = f"Name: {name}\nEmail: {email}\nSubject: {subject}\nMessage: {message}"
        try:
            # Send the email
            send_mail(
                f"New Contact Form Submission: {subject}",
                email_body,
                settings.DEFAULT_FROM_EMAIL,
                ['startyoung21@gmail.com'],
                fail_silently=False,
            )

            response_data = {'message': 'Message sent successfully!', 'status': 200}
            return JsonResponse(response_data)
        except Exception as e:
            response_data = {'message': e, 'status': 500}
            return JsonResponse(response_data)
    charity_number = (CharityDetail.objects.get(id=1)).charity_number
    email = (CharityDetail.objects.get(id=1)).email
    address = (CharityDetail.objects.get(id=1)).address
    phone_number = (CharityDetail.objects.get(id=1)).phone_number
    return render(
        request, "contact.html", {"opportunities": opportunities, "today": date.today(),"charity_number": charity_number,"email": email, "address":address, "phone_number":phone_number,} #"GSHEETS_CONTACT_US": settings.GSHEETS_CONTACT_US}
    )
