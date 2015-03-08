import json
import logging
from MuscleTracker import settings

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, Context, RequestContext
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.views import logout
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict
from django.contrib.auth.hashers import make_password
from django.template.loader import get_template
from django.core.mail import EmailMessage

from accounts.models import BetaEmail

logger = logging.getLogger("django.request")


@csrf_exempt
def saveEmail(request):
	rtn_dict = {'success': False, "msg": "", "created": False, 'email': ''}

	if request.method == 'POST':
		email = request.POST.get('email', False)

		if email:
			try:
				email_obj = BetaEmail.objects.get(email=email)
				rtn_dict['msg'] = 'Email {0} already submitted before'.format(email_object.email)
			except:
				email_obj = BetaEmail(email=email)
				try:
					email_obj.full_clean()
					email_obj.save()

					rtn_dict['msg'] = 'Successfully saved email {0}'.format(email_obj.email)
					rtn_dict['success'] = True
					rtn_dict['created'] = True
				except Exception as e:
					print 'Error saving email: {0}'.format(e)
					rtn_dict['msg'] = 'Error saving email: {0}'.format(e)


			rtn_dict['email'] = email_obj.email
		else:
			rtn_dict['msg'] = "'email' field not included in POST data"

	else:
		rtn_dict['msg'] = 'HTTP Method was not POST'

	return HttpResponse(json.dumps(rtn_dict), content_type="application/json")


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

	return HttpResponse(json.dumps(rtn_dict, cls=DjangoJSONEncoder), content_type="application/json")


@csrf_exempt
def registerUser(request):
	rtn_dict = {'success': False, "msg": ""}

	login_failed = False

	if request.method == 'POST':
		try:
			new_user = User(username=request.POST.get("username"))
			new_user.is_active = True
			new_user.password = make_password(request.POST.get('password1'))
			new_user.email = request.POST.get('email')
			new_user.save()
			user = authenticate(username=request.POST.get("username"), password=request.POST.get("password1"))

			if user is None:
				login_failed = True
				status = 401

			else:
				auth_login(request, user)
				account = Account(user=user)
				account.email = user.email
				account.user_name = user.username
				account.save()

				rtn_dict['success'] = True
				rtn_dict['msg'] = 'Successfully registered new user'
				rtn_dict['user'] = new_user.id
				rtn_dict['account'] = account.id
				return HttpResponse(json.dumps(rtn_dict, cls=DjangoJSONEncoder), content_type="application/json", status=status)

		except Exception as e:
			print 'Error registering new user: {0}'.format(e)
			logger.info('Error registering new user: {0}'.format(e))
			rtn_dict['msg'] = 'Error registering new user: {0}'.format(e)

	else:
		rtn_dict['msg'] = 'Not POST'

	return HttpResponse(json.dumps(rtn_dict, cls=DjangoJSONEncoder), content_type="application/json")


@csrf_exempt
def logoutUser(request):
	rtn_dict = {'success': False, "msg": ""}
	logout(request)
	if not request.user.is_authenticated():
		rtn_dict['success'] = True
	return HttpResponse(json.dumps(rtn_dict, cls=DjangoJSONEncoder), content_type="application/json")


def prepMailingList(email):
	mail_to = set()
	mail_to.add(email) 
	return mail_to


def prepBodyOfMail(email, activation_code):
	rtn_dict = {}
	rtn_dict['activation_code'] = activation_code
	return rtn_dict


def prepMail(subject, email):
    '''
        Sends a url to tryout app
    '''
    # get mail ID
    body = prepBodyOfMail(email, "example_activation_code")
    mail_to = prepMailingList(email)
    html_content = get_template('email/index-inline.html').render(Context(body))
    mail_from = settings.EMAIL_SENDER
    msg = EmailMessage(subject, html_content, mail_from, mail_to)
    msg.content_subtype = "html"  # Main content is now text/html; needs to be called after context is set
    
    return msg