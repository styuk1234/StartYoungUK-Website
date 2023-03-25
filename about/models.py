from django.db import models
import os
from django.core.validators import FileExtensionValidator

# Create your models here.
class TeamMember(models.Model):

    member_id = models.AutoField(primary_key=True)
    member_name = models.CharField(max_length=100, null=False)
    member_title = models.CharField(max_length=50, null=False)
    member_description = models.TextField(max_length=200, null=False)
    member_image = models.ImageField(default='default_member.jpg', upload_to='team_member_pics')

    def __str__(self) -> str:
        return f"{self.member_id, self.member_title}"
    
class GalleryItem(models.Model):
    
    item_id = models.AutoField(primary_key=True)
    item_title = models.CharField(max_length=100, null=False)
    item_file = models.FileField(default='default_image.jpg', upload_to='gallery_items',validators=[FileExtensionValidator(['mp4', 'mov', 'docx', 'jpg', 'png', 'jpeg'])])

    def __str__(self) -> str:
        return f"{self.item_id, self.item_title}"