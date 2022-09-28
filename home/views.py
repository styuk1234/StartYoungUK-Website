from django.shortcuts import render, redirect
from sponsor.models import Donation
from django.core.serializers import serialize
from django.contrib.auth.models import User
import json

def home(request):
    top_donation = Donation.objects.all().order_by('-amount')[:4]
    serial_donation= json.loads(serialize('json', top_donation))
    # print(serial_donation[1]['fields']['name'])
    cnt_usr = len(User.objects.all())
    return render(request, 'home.html', {'top_donations':serial_donation, 'cnt_usr': cnt_usr})

def buddysystem(request):
    return render (request, 'buddy.html')
