from django.shortcuts import render
from .models import TeamMember, GalleryImage
def about(request):
    members = TeamMember.objects.all()
    images = GalleryImage.objects.all()
    return render(request, 'about.html', {"members": members, "images": images})

