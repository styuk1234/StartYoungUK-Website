from django.db import models
#from PIL import Image
# Create your models here.

class Campaign(models.Model):

    campaign_id = models.AutoField(primary_key=True)
    campaign_title = models.CharField(max_length=50, null=False)
    campaign_description = models.TextField(max_length=200, null=False)
    collection_target = models.IntegerField(null=False)
    campaign_deadline = models.DateField(null=False)
    campaign_image = models.ImageField(default='default.jpg', upload_to='campaign_pics')

    def __str__(self):
        return f"{self.campaign_id, self.campaign_title}"

# TODO: discuss in database meeting how to store coporate sponsors, schools, etc
class Coporate_sponsors(models.Model):

    coporate_sponsor_id = models.AutoField(primary_key=True)
    coporate_sponsor_name = models.CharField(max_length=50, null=False)
    coporate_sponsor_description = models.TextField(max_length=200, null=False)
    # TODO: update upload_to to get corporate sponsor pics
    coporate_sponsor_image = models.ImageField(default='default.jpg', upload_to='campaign_pics')

    # def __str__(self):
    #     return f"{self.coporate_sponsor_id, self.coporate_sponsor_name}"