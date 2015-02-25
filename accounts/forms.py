from django import forms

from exercises.models import *
from django.forms.models import model_to_dict
from accounts.models import BetaEmail


class BetaEmailForm(forms.ModelForm):
	class Meta:
		model = BetaEmail