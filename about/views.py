import os
from django.shortcuts import render
from .models import TeamMember, GalleryItem
def about(request):
    members = TeamMember.objects.all()
    items = GalleryItem.objects.all()
    item_type = []
    for item in items:
        ext = os.path.splitext(item.item_file.name)[1].lower()
        if ext in ['.jpg', '.png', '.jpeg']:
            item_type.append('image')
        elif ext in ['.mp4', '.mov']:
            item_type.append('video')
        else:
            item_type.append('other')
    item_zip = zip(items,item_type)
    return render(request, 'about.html', {"members": members, "items": item_zip})

