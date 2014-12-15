from django.db import models
from accounts.models import Account
from workouts.models import WorkoutHistory, Workout

GENDER = (
    ('easy', 'Easy'),
    ('medium', 'Medium'),
    ('hard', 'Hard'),
)

# Create your models here.
class Muscle(models.Model):
	name = models.CharField(max_length=255)

	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)


class Equipment(models.Model):
	name = models.CharField(max_length=255)

	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)


class Exercise(models.Model):
	name = models.CharField(max_length=255)
	main_muscle = models.ForeignKey(Muscle)
	equipment = models.ForeignKey(Equipment, null=True, blank=True)
	difficulty = models.CharField(max_length=255)
	picture_url = models.CharField(max_length=255)
	rating = models.FloatField(null=True,blank=True)

	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)


class ExerciseHistory(models.Model):
	workout_history = models.ForeignKey(WorkoutHistory)
	exercise = models.ForeignKey(Exercise)
	order = models.IntegerField()
	sets = models.TextField()

	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)

	class Meta:
		unique_together = (('workout_history', 'order'),)