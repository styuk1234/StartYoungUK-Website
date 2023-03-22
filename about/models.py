from django.db import models

# Create your models here.
class TeamMember(models.Model):

    member_id = models.AutoField(primary_key=True)
    member_name = models.CharField(max_length=100, null=False)
    member_title = models.CharField(max_length=50, null=False)
    member_description = models.TextField(max_length=200, null=False)
    member_image = models.ImageField(default='default_member.jpg', upload_to='team_member_pics')

    def __str__(self):
        return f"{self.member_id, self.member_title}"
    
class GalleryImage(models.Model):

    IMAGE_TYPE = (
        ('image', 'Image'),
        ('video', 'Video')
    )
    
    image_id = models.AutoField(primary_key=True)
    image_title = models.CharField(max_length=100, null=False)
    gallery_image = models.FileField(default='default_image.jpg', upload_to='gallery_pics')
    gallery_type = models.CharField(max_length=5, choices=IMAGE_TYPE, default='image')

    def __str__(self):
        return f"{self.image_id, self.image_title}"
