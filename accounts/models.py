from django.db import models
from django.contrib.auth.models import User
# Create your models here.
GENDER = (
    ('male', 'Male'),
    ('female', 'Female'),
)

# Create your models here.
class Account(models.Model):
	user = models.OneToOneField(User)
	user_name = models.CharField(max_length=255, unique=True)
	display_name = models.CharField(max_length=255, null=True, blank=True)
	first_name = models.CharField(max_length=255, null=True, blank=True)
	last_name = models.CharField(max_length=255, null=True, blank=True)
	phone_number = models.CharField(max_length=255, null=True, blank=True, unique=True)
	email = models.CharField(max_length=255, unique=True)
	bio = models.CharField(max_length=255, null=True, blank=True)
	gender = models.CharField(max_length=255, null=True, blank=True, choices=GENDER)
	birthday = models.DateField(null=True,blank=True)
	is_active = models.NullBooleanField(default=True)

	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)
	def __unicode__(self):
		return str('{0}'.format(self.user_name))


class BetaEmail(models.Model):
	email = models.EmailField(max_length=75, unique=True)
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)
	def __unicode__(self):
		return str('{0}'.format(self.email))