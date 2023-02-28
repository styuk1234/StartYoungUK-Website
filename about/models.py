from django.db import models

# Create your models here.
class Team_members(models.Model):

    member_id = models.AutoField(primary_key=True)
    member_name = models.CharField(max_length=100, null=False)
    member_title = models.CharField(max_length=50, null=False)
    member_description = models.TextField(max_length=200, null=False)
    member_image = models.ImageField(default='default_member.jpg', upload_to='team_member_pics')

    def __str__(self):
        return f"{self.member_id, self.member_title}"
