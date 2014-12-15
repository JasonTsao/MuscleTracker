import json
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import User
from accounts.models import Account
from django.views.decorators.csrf import csrf_exempt

def getExcercise(request, exercise_id):
	rtn_dict = {'success': False, "msg": ""}

	return HttpResponse(json.dumps(rtn_dict, cls=DjangoJSONEncoder), content_type="application/json")