import json
import logging
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import User
from accounts.models import Account
from workouts.models import Workout, WorkoutHistory
from models import Exercise, ExerciseHistory, Muscle, Equipment
from django.views.decorators.csrf import csrf_exempt


@login_required
def getExercise(request, exercise_id):
	rtn_dict = {'success': False, "msg": ""}

	try:
		if not request.user.id:
			user_id = request.POST['user']
		else:
			user_id = request.user.id

		account = Account.objects.get(user__id=user_id)
		exercise = Exercise.objects.get(pk=exercise_id)
		rtn_dict['exercise'] = model_to_dict(exercise)
	except Exception as e:
		print e
		logger.info('Error grabbing exercise {0}: {1}'.format(exercise_id, e))
		rtn_dict['msg'] = 'Error grabbing exercise {0}: {1}'.format(exercise_id, e)

	return HttpResponse(json.dumps(rtn_dict, cls=DjangoJSONEncoder), content_type="application/json")


@login_required
def getExercises(request):
	rtn_dict = {'success': False, "msg": ""}

	try:
		if not request.user.id:
			user_id = request.POST['user']
		else:
			user_id = request.user.id

		account = Account.objects.get(user__id=user_id)
		exercises = Exercise.objects.filter(account=account)
		rtn_dict['exercises'] = [model_to_dict(exercise) for exercise in exercises]
	except Exception as e:
		print e
		logger.info('Error grabbing exercises {0}: {1}'.format(workout_id, e))
		rtn_dict['msg'] = 'Error grabbing exercises {0}: {1}'.format(workout_id, e)

	return HttpResponse(json.dumps(rtn_dict, cls=DjangoJSONEncoder), content_type="application/json")


@login_required
def getExerciseHistory(request, exercise_id):
	rtn_dict = {'success': False, "msg": ""}

	try:
		if not request.user.id:
			user_id = request.POST['user']
		else:
			user_id = request.user.id

		account = Account.objects.get(user__id=user_id)
		exercise_history = ExerciseHistory.objects.get(pk=exercise_id, account=account)

		rtn_dict['exercise_history'] = model_to_dict(exercise_history)

	except Exception as e:
		print e
		logger.info('Error grabbing exercise history {0}: {1}'.format(exercise_id, e))
		rtn_dict['msg'] = 'Error grabbing exercise history {0}: {1}'.format(exercise_id, e)

	return HttpResponse(json.dumps(rtn_dict, cls=DjangoJSONEncoder), content_type="application/json")


@login_required
def getExerciseHistories(request, workout_id):
	rtn_dict = {'success': False, "msg": ""}

	try:
		if not request.user.id:
			user_id = request.POST['user']
		else:
			user_id = request.user.id

		account = Account.objects.get(user__id=user_id)
		workout_history = WorkoutHistory.objects.get(pk=workout_id, account=account)
		exercise_histories = ExerciseHistory.objects.filter(workout_history=workout_history)

		rtn_dict['exercise_histories'] = [model_to_dict(exercise) for exercise in exercise_histories]

	except Exception as e:
		print e
		logger.info('Error grabbing exercise history {0}'.format(e))
		rtn_dict['msg'] = 'Error grabbing exercise history {0}'.format(e)

	return HttpResponse(json.dumps(rtn_dict, cls=DjangoJSONEncoder), content_type="application/json")


@login_required
def saveExercise(request):
	rtn_dict = {'success': False, "msg": ""}
	return HttpResponse(json.dumps(rtn_dict, cls=DjangoJSONEncoder), content_type="application/json")


@login_required
def addExerciseHistoryToWorkout(request):
	rtn_dict = {'success': False, "msg": "", "exercise_history_id":None}

	if request.method == 'POST':
		try:
			if not request.user.id:
				user_id = request.POST['user']
			else:
				user_id = request.user.id

			account = Account.objects.get(user__id=user_id)

			workout_history = WorkoutHistory.objects.get(request.POST['workout_history_id'], account=account)
			count = ExerciseHistory.objects.filter(workout_history=workout_history).count()
			exercise_history = ExerciseHistory(workout_history=workout_history, exercise=exercise_item['exercise_id'], order=count)
			exercise_history.sets = request.POST['sets']
			exercise_history.save()
			exercise_history_ids.append(exercise_history.id)

			rtn_dict['exercise_history_id'] = workout_history.id
		except Exception as e:
			print e
			logger.info('Error grabbing exercise histories {0}'.format(e))
			rtn_dict['msg'] = 'Error grabbing exercise histories {0}'.format(e)
	else:
		rtn_dict['msg'] = 'Not POST'

	return HttpResponse(json.dumps(rtn_dict, cls=DjangoJSONEncoder), content_type="application/json")


@login_required
def editExerciseHistory(request):
	rtn_dict = {'success': False, "msg": ""}
	if request.method == 'POST':
		try:
			if not request.user.id:
				user_id = request.POST['user']
			else:
				user_id = request.user.id

			account = Account.objects.get(user__id=user_id)

			#Check to see if user who's requesting to change is allowed to edit exercise
			workout_history = WorkoutHistory.objects.get(request.POST['workout_history_id'], account=account)

			exercise_history = ExerciseHistory.objects.get(workout_history=workout_history, pk=request.POST['exercise_history_id'])

			exercise_id = request.POST.get('exercise_id', False)

			if exercise_id:
				exercise = Exercise.objects.get(pk=request.POST['exercise_id'])
				exercise_history.exercise = exercise

			exercise_history.sets = request.POST['sets']
			exercise_history.save()

		except Exception as e:
			print e
			logger.info('Error editing exercise histories {0}'.format(e))
			rtn_dict['msg'] = 'Error grabbing exercise histories {0}'.format(e)

	else:
		rtn_dict['msg'] = 'Not POST'

	return HttpResponse(json.dumps(rtn_dict, cls=DjangoJSONEncoder), content_type="application/json")