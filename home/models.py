from django.db import models

# Create your models here.

class Campaigns(models.Model):
    #title, donation, target_money,
    #campaign ID to be noted, so that donation can be tracked
    #donation table needs an identifier
    campaign_id = models.AutoField(primary_key=True)
    campaign_title = models.CharField(max_length=50, null=False)
    campaign_description = models.TextField(max_length=200, null=False)
    collection_target = models.IntegerField(null=False)
    campaign_image = models.ImageField(default='default.jpg', upload_to='campaign_pics')

    def __str__(self):
        return f"{self.campaign_id, self.campaign_title}" 