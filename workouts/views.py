import json
from django.contrib.auth.models import User

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse


def newWorkout(request):
	return render_to_response('workouts/new_workout.html', {}, context_instance=RequestContext(request))