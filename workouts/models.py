from django.db import models
from accounts.models import Account

# Create your models here.
class Workout(models.Model):
	account = models.ForeignKey(Account)
	name = models.CharField(max_length=255)
	exercises = models.ManyToManyField('exercises.Excercise')

	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)


class WorkoutHistory(models.Model):
	account = models.ForeignKey(Account)
	date =  models.DateTimeField()
	name = models.CharField(max_length=255)

	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)