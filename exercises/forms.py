from django import forms

from exercises.models import *
from django.forms.models import model_to_dict
from accounts.models import Account


class BodyPartForm(forms.ModelForm):
	class Meta:
		model = BodyPart


class MuscleForm(forms.ModelForm):
	class Meta:
		model = Muscle


class EquiptmentForm(forms.ModelForm):
	class Meta:
		model = Equipment


class ExerciseForm(forms.ModelForm):
	class Meta:
		model = Exercise
		fields = ('name', 'main_muscle')


class ExerciseHistoryForm(forms.ModelForm):
	class Meta:
		model = ExerciseHistory