from django.db import models
from django.contrib.auth.models import (
    User, BaseUserManager, AbstractBaseUser
)
# Don't forget to migrate when editing/creating models :)

# Create your models here.
'''
class Tweet(models.Model):
    body = models.TextField(max_length=300)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField()

    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='likes', blank=True)

    def __str__(self):
        return self.body
'''

# tutorial: https://www.codingforentrepreneurs.com/blog/how-to-create-a-custom-django-user-model
class ProfileManager(BaseUserManager):
    def create_profile(self, username, email, password=None):
        #creates and saves a user with the given email and pw
        if not email:
            raise ValueError('Profile must have an email address')
        profile = self.model(
            username = username,
            email = self.normalize_email(email),
        )

        profile.set_password(password)
        profile.save(using=self.db)
        return profile
    
    def create_teacher(self, username, email, password):
        teacher = self.create_profile(username = username, email = email, password=password)
        teacher.teacher = True
        teacher.save(using=self._db)
        return teacher

    def create_superuser(self, email, password):
        superuser = self.create_profile(username = email, email = email, password = password)
        superuser.admin = True
        superuser.is_staff = True
        superuser.save(using=self._db)
        return superuser

class Profile(AbstractBaseUser):
    username = models.TextField(max_length=20)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    admin = models.BooleanField(default=False) # a superuser
    staff = models.BooleanField(default=False)
    teacher = models.BooleanField(default=False) # student or teacher
    password = models.TextField(max_length=20)
    objects = ProfileManager()

    USERNAME_FIELD = 'email' #how django recognizes the user
    REQUIRED_FIELDS = [] #email and pw required by default
    #pw field is built in

    def is_teacher(self):
        return self.teacher

    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    def is_admin(self):
        "Is the user a admin member?"
        return self.admin
    
    def __str__(self):
        return self.email

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    
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
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField()

    def __str__(self):
        return self.student_request
    
    def __repr__(self):
        return self.student_request