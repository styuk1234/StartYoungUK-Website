from django.shortcuts import render
from home.models import Opportunity
from datetime import date
from django.conf import settings


def contact(request):
    opportunities = Opportunity.objects.all()

    return render(
        request, "contact.html", {"opportunities": opportunities, "today": date.today(), "GSHEETS_CONTACT_US": settings.GSHEETS_CONTACT_US}
    )
