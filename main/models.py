from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Don't forget to migrate when editing/creating models :)
   
class Profile(models.Model):
    # class AccountType(models.TextChoices):
    #     TEACHER = 'TE', _('Teacher')
    #     STUDENT = 'ST', _('Student')

    # REQUIRED_FIELDS = ('user',)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    accountType = models.CharField(default="student", max_length=50)
    # models.CharField(
    #     max_length=2, # can rmv this line later
    #     choices=AccountType.choices,
    #     default=AccountType.STUDENT,
    # )

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