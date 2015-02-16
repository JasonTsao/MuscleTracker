from django.db import models
from accounts.models import Account

# Create your models here.
class Workout(models.Model):
	account = models.ForeignKey(Account)
	name = models.CharField(max_length=255)
	exercises = models.ManyToManyField('exercises.Exercise')

	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)
	def __unicode__(self):
		return '{0} : {1}'.format(self.account.user_name, self.name)


class WorkoutHistory(models.Model):
	account = models.ForeignKey(Account)
	date =  models.DateTimeField()
	name = models.CharField(max_length=255)
	exercise_histories = models.ManyToManyField('exercises.ExerciseHistory')

	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)

	def __unicode__(self):
		return '{0} : {1}: {2}'.format(self.account.user_name, self.name, self.date)