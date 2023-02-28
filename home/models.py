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

class Affiliation(models.Model):

    affiliation_id = models.AutoField(primary_key=True)
    affiliation_name = models.CharField(max_length=50, null=False)
    affiliation_description = models.TextField(max_length=200, null=False)
    # TODO: update upload_to to get corporate sponsor pics
    affiliation_image = models.ImageField(default='default.jpg', upload_to='affiliation_pics')
    affiliation_join_date = models.DateField(null=False)
    affiliation_display = models.BooleanField(null=False)

    def __str__(self):
        return f"{self.affiliation_id, self.affiliation_name}"
class Opportunity(models.Model):

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, null=False)
    description = models.TextField(max_length=400, null=False)
    end_date = models.DateField(null=False)
    salary = models.IntegerField(null=False)
    duration = models.TextField(max_length=50, null=False)
    form_url = models.URLField(max_length=100, null=False)
    position_filled = models.BooleanField(null=False, default=False)

    def __str__(self):
        return f"{self.id, self.title}"
