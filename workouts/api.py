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
		rtn_dict['success'] = True
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
		rtn_dict['success'] = True
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
		rtn_dict['success'] = True
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
		rtn_dict['success'] = True
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

			account = Account.objects.get(pk=request.POST['account'])
			workout = Workout(name=request.POST['name'], account=account)
			workout.save()

			for exercise_id in request.POST.getlist('exercises[]'):
				exercise = Exercise.objects.get(pk=exercise_id)
				workout.exercises.add(exercise)
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
	rtn_dict = {'success': False, "msg": "", 'workout_history_id':None}

	if request.method == 'POST':
		workout_id = request.POST.get('workout', False)
		exercises = request.POST.getlist('exercises[]')
		exercise_sets = request.POST.get('exercise_sets', False)

		if exercises and workout_id and exercise_sets:
			try:
				if not request.user.id:
					user_id = request.POST['user']
				else:
					user_id = request.user.id

				exercise_sets = json.loads(exercise_sets)

				account = Account.objects.get(user__id=user_id)
				workout = Workout.objects.get(pk=workout_id)
				workout_history = WorkoutHistory(account=account,workout=workout)
				workout_history.save()

				count = 0
				for exercise_id in exercises:
					exercise = Exercise.objects.get(pk=exercise_id)
					exercise_history = ExerciseHistory(workout_history=workout_history, exercise=exercise, order=count)
					exercise_history.sets = exercise_sets[exercise_id]
					exercise_history.save()
					count +=1

				rtn_dict['success'] = True
			except Exception as e:
				print e
				logger.info('Error grabbing workout histories {0}'.format(e))
				rtn_dict['msg'] = 'Error grabbing workout histories {0}'.format(e)
		else:
			rtn_dict['msg'] = "Submit form data invalid"
	else:
		rtn_dict['msg'] = 'Not POST'

	return HttpResponse(json.dumps(rtn_dict, cls=DjangoJSONEncoder), content_type="application/json")


@login_required
def saveExerciseToWorkoutHistory(request):
	rtn_dict = {'success': False, "msg": ""}

	if request.method == "POST":
		workout_history_id = request.POST.get('workout_history', False)
		exercises = request.POST.getlist('exercises[]')
		exercise_sets = request.POST.get('exercise_sets', False)

		if exercises and workout_history_id and exercise_sets:
			try:
				count = 0
				workout_history = WorkoutHistory.objects.get(pk=workout_history_id)
				for exercise_id in exercises:
					exercise = Exercise.objects.get(pk=exercise_id)
					exercise_history = ExerciseHistory(workout_history=workout_history, exercise=exercise, order=count)
					exercise_history.sets = exercise_sets[exercise_id]
					exercise_history.save()
					count +=1

				rtn_dict['success'] = True
			except Exception as e:
				print 'Error saving an exercise history to a workout history: {0}'.format(e)
				rtn_dict['msg'] = 'Error saving an exercise history to a workout history: {0}'.format(e) 
	else:
		rtn_dict['msg'] = 'Not POST'
	return HttpResponse(json.dumps(rtn_dict, cls=DjangoJSONEncoder), content_type="application/json")