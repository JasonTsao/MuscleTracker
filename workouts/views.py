import json
from django.contrib.auth.models import User

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse

from workouts.forms import *

def newWorkout(request):
	return render_to_response('workouts/new_workout.html', {"form":WorkoutForm()}, context_instance=RequestContext(request))


def newWorkoutHistory(request):
	return render_to_response('workouts/new_workout_history.html', {"form":WorkoutHistoryForm(), "workout_form":WorkoutForm()}, context_instance=RequestContext(request))