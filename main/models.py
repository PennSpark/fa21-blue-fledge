from django.db import models
from django.contrib.auth.models import User
# Don't forget to migrate when editing/creating models :)

# Create your models here.
class Tweet(models.Model):
    body = models.TextField(max_length=300)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField()

    likes = models.ManyToManyField(User, related_name='likes', blank=True)

    def __str__(self):
        return self.body


# https://docs.djangoproject.com/en/dev/ref/models/fields/#choices
# ^ More info on choices/enum
class Confusion(models.Model):
    CONFUSE_CHOICES = [
        ('GEN', 'General'),
        ('SLOW', 'Slow Down'),
        ('REP', 'Repeat That'),
        ('REPHR', 'Rephrase'),
        ('EX', 'Provide An Example'),
        ('OTHER', 'Other'),
    ]
    student_request = models.CharField(max_length=5, choices = CONFUSE_CHOICES, default = 'GEN')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField()

    def __str__(self):
        return self.student_request
    
    def __repr__(self):
        return self.student_request