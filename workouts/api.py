import json
import logging
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import User

from models import Workout, WorkoutHistory
from accounts.models import Account
from exercises.models import Exercise, ExerciseHistory 

from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger("django.request")


@login_required
def getWorkout(request, workout_id):
	rtn_dict = {'success': False, "msg": ""}
	return HttpResponse(json.dumps(rtn_dict, cls=DjangoJSONEncoder), content_type="application/json")


@login_required
def getWorkouts(request, workout_id):
	rtn_dict = {'success': False, "msg": ""}
	return HttpResponse(json.dumps(rtn_dict, cls=DjangoJSONEncoder), content_type="application/json")


@login_required
def getWorkoutHistory(request, workout_id):
	rtn_dict = {'success': False, "msg": ""}

	try:
		if not request.user.id:
			user_id = request.POST['user']
		else:
			user_id = request.user.id

		account = Account.objects.get(user__id=user_id)
		workout_history = WorkoutHistory.objects.get(pk=workout_id, account=account)
		exercise_histories = ExerciseHistory.objects.filter(workout_history=workout_history)

		exercise_histories = [model_to_dict(x) for x in exercise_histories]

		rtn_dict['workout_history'] = model_to_dict(workout_history)
		rtn_dict['exercise_histories'] = exercise_histories

	except Exception as e:
		print e
		logger.info('Error grabbing workout {0}: {1}'.format(workout_id, e))
		rtn_dict['msg'] = 'Error grabbing workout {0}: {1}'.format(workout_id, e)

	return HttpResponse(json.dumps(rtn_dict, cls=DjangoJSONEncoder), content_type="application/json")


@login_required
def getWorkoutHistories(request):
	rtn_dict = {'success': False, "msg": ""}

	try:
		if not request.user.id:
			user_id = request.POST['user']
		else:
			user_id = request.user.id

		account = Account.objects.get(user__id=user_id)
		workout_histories = WorkoutHistory.objects.filter(account=account)

		rtn_dict['workout_histories'] = model_to_dict(workout_histories)

	except Exception as e:
		print e
		logger.info('Error grabbing workouts {0}: {1}'.format(workout_id, e))
		rtn_dict['msg'] = 'Error grabbing workouts {0}: {1}'.format(workout_id, e)

	return HttpResponse(json.dumps(rtn_dict, cls=DjangoJSONEncoder), content_type="application/json")