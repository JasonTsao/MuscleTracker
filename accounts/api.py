import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, Context, RequestContext
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.views import logout
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict
from django.contrib.auth.hashers import make_password


@csrf_exempt
def login(request):
	rtn_dict = {'success': False, "msg": ""}

	login_failed = False

	if request.method == "POST":
 		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				auth_login(request, user)
			else:
				return HttpResponseForbidden(\
					content='Your account is not active.')

			status = 200
		else:
			login_failed = True
			status = 401

		try:
			account = Account.objects.get(user=user)
			rtn_dict['userid'] = account.id
		except Exception as e:
			print 'Unable to get account for user id {0}'.format(e)
			logger.info('Unable to get account for user id {0}'.format(e))

		return HttpResponse(json.dumps(rtn_dict, cls=DjangoJSONEncoder), content_type="application/json", status=status)

		#if login_failed:
		#	response['Auth-Response'] = 'Login failed'
	'''
	if request.user.is_authenticated():
		status = 200
	else:
		status = 401
	'''

	'''
	response = render_to_response('accounts/login.html', {"rtn_dict":rtn_dict},
                                  context_instance=RequestContext(request))
	response.status_code = status
	if login_failed:
		response['Auth-Response'] = 'Login failed''
	'''
	return HttpResponse(json.dumps(rtn_dict, cls=DjangoJSONEncoder), content_type="application/json")