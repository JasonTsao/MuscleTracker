import json
import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import User
from accounts.models import Account
from models import MuscleLoad
from django.views.decorators.csrf import csrf_exempt

def getLatestMuscleLoad(request, muscle_load_id):
	rtn_dict = {'success': False, "msg": ""}

	try:
		if not request.user.id:
			user_id = request.POST['user']
		else:
			user_id = request.user.id

		account = Account.objects.get(user__id=user_id)
		muscle_load = MuscleLoad.objects.get(pk=muscle_load_id)
		rtn_dict['muscle_load'] = model_to_dict(muscle_load)
	except Exception as e:
		print e
		logger.info('Error grabbing latest muscle load {0}: {1}'.format(muscle_load_id, e))
		rtn_dict['msg'] = 'Error grabbing latest muscle load {0}: {1}'.format(muscle_load_id, e)

	return HttpResponse(json.dumps(rtn_dict, cls=DjangoJSONEncoder), content_type="application/json")


def getMuscleLoads(request, start_date, end_date):
	rtn_dict = {'success': False, "msg": ""}

	try:
		if not request.user.id:
			user_id = request.POST['user']
		else:
			user_id = request.user.id

		account = Account.objects.get(user__id=user_id)
		muscle_loads = MuscleLoad.objects.filter(date__gte=start_date, date__lte=end_date)
		rtn_dict['muscle_loads'] = [model_to_dict(muscle_load) for muscle_load in muscle_loads]
	except Exception as e:
		print e
		logger.info('Error grabbing latest muscle loads {0}: {1}'.format(muscle_load_id, e))
		rtn_dict['msg'] = 'Error grabbing latest muscle loads {0}: {1}'.format(muscle_load_id, e)

	return HttpResponse(json.dumps(rtn_dict, cls=DjangoJSONEncoder), content_type="application/json")


@login_required
def saveMuscleLoad(request):
	rtn_dict = {'success': False, "msg": ""}

	if request.method == 'POST':
		try:
			if not request.user.id:
				user_id = request.POST['user']
			else:
				user_id = request.user.id

			account = Account.objects.get(user__id=user_id)
			muscle_load, created = MuscleLoad.objects.get_or_create(account=account, date=datetime.datetime.now)

			if created:
				#save all values directly into muscle load
				pass
			else:
				#add new values to previous value for this date
				pass
			muscle_load.save()

			rtn_dict['success'] = True
		except Exception as e:
			print 'Unable to save Muscle Load: {0}'.format(e)
			logger.info('Unable to save Muscle Load: {0}'.format(e))
			rtn_dict['msg'] = 'Unable to save Muscle Load: {0}'.format(e)
	else:
		rtn_dict['msg'] = 'request method was not POST'

	return HttpResponse(json.dumps(rtn_dict, cls=DjangoJSONEncoder), content_type="application/json")