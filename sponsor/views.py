from django.shortcuts import render

def sponsor(request):
    return render(request, 'sponsor.html')