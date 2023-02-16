from django.db import models
#from PIL import Image
# Create your models here.

class Campaign(models.Model):

    campaign_id = models.AutoField(primary_key=True)
    campaign_title = models.CharField(max_length=50, null=False)
    campaign_description = models.TextField(max_length=200, null=False)
    collection_target = models.IntegerField(null=False)
    campaign_deadline = models.DateField(null=False)
    campaign_image = models.ImageField(default='campaign_pics/default_campaign.jpg', upload_to='campaign_pics')

    def __str__(self):
        return f"{self.campaign_id, self.campaign_title}"

class Opportunity(models.Model):

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, null=False)
    description = models.TextField(max_length=400, null=False)
    form_url = models.URLField(max_length=100, null=False)

    def __str__(self):
        return f"{self.id, self.title}"