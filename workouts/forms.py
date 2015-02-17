from django import forms

from workouts.models import *
from django.forms.models import model_to_dict
from accounts.models import Account


class WorkoutForm(forms.ModelForm):
	class Meta:
		model = Workout


class WorkoutHistoryForm(forms.ModelForm):
	class Meta:
		model = WorkoutHistory



