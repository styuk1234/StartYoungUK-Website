from django.db import models
from django.urls import reverse

class Campaign(models.Model):

    campaign_id = models.AutoField(primary_key=True)
    campaign_title = models.CharField(max_length=50, null=False)
    campaign_description = models.TextField(max_length=200, null=False)
    collection_target = models.IntegerField(null=False)
    campaign_deadline = models.DateField(null=False)
    campaign_image = models.ImageField(default='campaign_pics/default_campaign.jpg', upload_to='campaign_pics')
    is_active = models.BooleanField(null=False, default=True)
    slug = models.SlugField(null=False, unique=True)

    def __str__(self):
        return f"{self.campaign_id, self.campaign_title}"
    
    def get_absolute_url(self):
        return reverse("campaign-donate", kwargs={"slug": self.slug})


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
    job_paid = models.BooleanField(null=False, default=False)
    duration = models.TextField(max_length=50, null=False)
    form_url = models.URLField(max_length=100, null=False)
    position_filled = models.BooleanField(null=False, default=False)

    def __str__(self):
        return f"{self.id, self.title}"

class EmailContent(models.Model):
    id = models.AutoField(primary_key=True)
    email_type = models.CharField(choices=[('Approve', 'Buddy Approval Email'), ('Reject', 'Buddy Rejection Email'), ('Letter', 'Buddy Letter Reminder')], max_length=50)
    subject = models.CharField(max_length=100, null=False)
    header = models.CharField(max_length=255, null=False)
    body = models.TextField()
    attachment = models.FileField(blank=True, upload_to='attachments/')
    attachment2 = models.FileField(blank=True, upload_to='attachments/')
    attachment3 = models.FileField(blank=True, upload_to='attachments/')
    attachment4 = models.FileField(blank=True, upload_to='attachments/')
    attachment5 = models.FileField(blank=True, upload_to='attachments/')
    signature = models.TextField()