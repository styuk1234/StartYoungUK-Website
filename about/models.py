from django.db import models
import os
from .validators import validate_file_extension

# Create your models here.
class TeamMember(models.Model):

    member_id = models.AutoField(primary_key=True)
    member_name = models.CharField(max_length=100, null=False)
    member_title = models.CharField(max_length=50, null=False)
    member_description = models.TextField(max_length=200, null=False)
    member_image = models.ImageField(default='default_member.jpg', upload_to='team_member_pics')

    def __str__(self):
        return f"{self.member_id, self.member_title}"
    
class GalleryItem(models.Model):
    
    item_id = models.AutoField(primary_key=True)
    item_title = models.CharField(max_length=100, null=False)
    item_file = models.FileField(default='default_image.jpg', upload_to='gallery_items',validators=[validate_file_extension])
    # item_type = models.CharField(max_length=5, default='image')

    # def save(self, *args, **kwargs):
    #     ext = os.path.splitext(self.item_file.name)[1][1:].lower()

    #     if ext in ['jpg', 'jpeg', 'png', 'gif']:
    #         self.item_type = 'image'
    #     elif ext in ['mp4', 'avi', 'mov']:
    #         self.item_type = 'video'
    #     else:
    #         self.item_type = 'other'

    #     super(GalleryItem, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.item_id, self.item_title}"