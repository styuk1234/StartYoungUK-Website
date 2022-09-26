from django.shortcuts import render
from sponsor.models import Donation
from django.core.serializers import serialize
import json

def home(request):
    top_donation = Donation.objects.all().order_by('-amount')[:4]
    serial_donation= json.loads(serialize('json', top_donation))
    # print(serial_donation[1]['fields']['name'])
    return render(request, 'home.html', {'top_donations':serial_donation})