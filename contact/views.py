from django.shortcuts import render
from home.models import Opportunity
from datetime import date


def contact(request):
    opportunities = Opportunity.objects.all()

    return render(
        request, "contact.html", {"opportunities": opportunities, "today": date.today()}
    )
