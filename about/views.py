from django.shortcuts import render
from .models import TeamMember
def about(request):
    members = TeamMember.objects.all()
    return render(request, 'about.html', {"members": members})