from django.shortcuts import render
from sponsor.models import Donation
from django.core.serializers import serialize
import json

def home(request):
    top10_donation = Donation.objects.all().order_by('amount')[:10]
    serial_donation= json.loads(serialize('json', top10_donation))
    print(serial_donation)
    return render(request, 'home.html')