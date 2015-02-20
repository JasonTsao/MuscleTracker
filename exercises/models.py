from django.db import models
from accounts.models import Account
from workouts.models import WorkoutHistory, Workout

DIFFICULTY = (
    ('easy', 'Easy'),
    ('medium', 'Medium'),
    ('hard', 'Hard'),
)


class BodyPart(models.Model):
	name = models.CharField(max_length=255, unique=True)
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)
	def __unicode__(self):
		return self.name


class Muscle(models.Model):
	name = models.CharField(max_length=255, unique=True)
	body_part = models.ForeignKey(BodyPart, null=True,blank=True)
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)
	def __unicode__(self):
		return self.name


class Equipment(models.Model):
	name = models.CharField(max_length=255, unique=True)

	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)
	def __unicode__(self):
		return self.name


class Exercise(models.Model):
	name = models.CharField(max_length=255, unique=True)
	main_muscle = models.ForeignKey(Muscle)
	equipment = models.ForeignKey(Equipment, null=True, blank=True)
	difficulty = models.CharField(max_length=255)
	picture_url = models.CharField(max_length=255)
	rating = models.FloatField(null=True,blank=True)

	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)
	def __unicode__(self):
		if self.equipment:
			return '{0} : {1}: {2}'.format(self.name, self.main_muscle.name, self.equipment.name)
		else:
			return '{0} : {1}'.format(self.name, self.main_muscle.name)


class ExerciseHistory(models.Model):
	workout_history = models.ForeignKey(WorkoutHistory, null=True, blank=True)
	exercise = models.ForeignKey(Exercise)
	order = models.IntegerField(null=True,blank=True)
	sets = models.TextField()

	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True, blank=True, null=True)

	class Meta:
		unique_together = (('workout_history', 'order'),)
	def __unicode__(self):
		return '{0} : {1}'.format(self.workout_history.workout.name, self.exercise.name)