import json
import logging
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import User

from models import Workout, WorkoutHistory
from forms import WorkoutForm, WorkoutHistoryForm
from accounts.models import Account
from exercises.models import Exercise, ExerciseHistory 

from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger("django.request")


@login_required
def getWorkout(request, workout_id):
	rtn_dict = {'success': False, "msg": ""}

	try:
		if not request.user.id:
			user_id = request.POST['user']
		else:
			user_id = request.user.id

		account = Account.objects.get(user__id=user_id)
		workout = Workout.objects.get(pk=workout_id)
		rtn_dict['workout'] = model_to_dict(workout)
	except Exception as e:
		print e
		logger.info('Error grabbing workout {0}: {1}'.format(workout_id, e))
		rtn_dict['msg'] = 'Error grabbing workout {0}: {1}'.format(workout_id, e)

	return HttpResponse(json.dumps(rtn_dict, cls=DjangoJSONEncoder), content_type="application/json")


@login_required
def getWorkouts(request):
	rtn_dict = {'success': False, "msg": ""}

	try:
		if not request.user.id:
			user_id = request.POST['user']
		else:
			user_id = request.user.id

		account = Account.objects.get(user__id=user_id)
		workouts = Workout.objects.filter(account=account)
		rtn_dict['workout'] = [model_to_dict(workout) for workout in workouts]
	except Exception as e:
		print e
		logger.info('Error grabbing workouts {0}: {1}'.format(workout_id, e))
		rtn_dict['msg'] = 'Error grabbing workouts {0}: {1}'.format(workout_id, e)

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
		logger.info('Error grabbing workout history {0}: {1}'.format(workout_id, e))
		rtn_dict['msg'] = 'Error grabbing workout history {0}: {1}'.format(workout_id, e)

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
		logger.info('Error grabbing workout histories {0}'.format(e))
		rtn_dict['msg'] = 'Error grabbing workout histories {0}'.format(e)

	return HttpResponse(json.dumps(rtn_dict, cls=DjangoJSONEncoder), content_type="application/json")


@login_required
def saveWorkout(request):
	rtn_dict = {'success': False, "msg": ""}

	if request.method == 'POST':
		try:
			if not request.user.id:
				user_id = request.POST['user']
			else:
				user_id = request.user.id

			account = Account.objects.get(user__id=user_id)
			workout = Workout()
			form = WorkoutForm(request.POST['workout'], instance=workout)

			if form.is_valid():
				for exercise_id in request.POST['exercises']:
					exercise = Exercise.objects.get(pk=exercise_id)
					workout.exercises.add(exercise)
				workout.save()
				rtn_dict['success'] = True
		except Exception as e:
			print e
			logger.info('Error saving workout {0}'.format(e))
			rtn_dict['msg'] = 'Error saving workout {0}'.format(e)
	else:
		rtn_dict['msg'] = 'Not POST'

	return HttpResponse(json.dumps(rtn_dict, cls=DjangoJSONEncoder), content_type="application/json")


@login_required
def saveWorkoutHistory(request):
	rtn_dict = {'success': False, "msg": "", "exercise_history_ids":[], 'workout_history_id':None}

	if request.method == 'POST':
		try:
			if not request.user.id:
				user_id = request.POST['user']
			else:
				user_id = request.user.id

			account = Account.objects.get(user__id=user_id)
			workout_history = WorkoutHistory(request.POST['workout_history'])
			workout_history.save()

			exercise_histories = request.POST.get('exercises', False)

			if exercise_histories:
				count = 0
				exercise_history_ids = []
				for exercise_item in exercise_histories:
					exercise_history = ExerciseHistory(workout_history=workout_history, exercise=exercise_item['exercise_id'], order=count)
					exercise_history.sets = request.POST['sets']
					exercise_history.save()
					exercise_history_ids.append(exercise_history.id)
					count +=1
					rtn_dict['exercise_history_ids'] = exercise_history_ids

			rtn_dict['workout_history_id'] = workout_history.id
		except Exception as e:
			print e
			logger.info('Error grabbing workout histories {0}'.format(e))
			rtn_dict['msg'] = 'Error grabbing workout histories {0}'.format(e)
	else:
		rtn_dict['msg'] = 'Not POST'

	return HttpResponse(json.dumps(rtn_dict, cls=DjangoJSONEncoder), content_type="application/json")