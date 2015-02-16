import json
from django.contrib.auth.models import User

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse

from exercises.forms import *

def newExercise(request):
	return render_to_response('exercises/new_exercise.html', {"form": ExerciseForm()}, context_instance=RequestContext(request))