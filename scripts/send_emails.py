import json
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from accounts.api import prepMail

from accounts.models import BetaEmail

from django.views.decorators.csrf import csrf_exempt


def sendBetaAppEmails(request):
	rtn_dict = {'success': False, "msg": ""}

	try:
		beta_emails = BetaEmail.objects.all()

		beta_emails_array = [beta_email.email for beta_email in beta_emails]
			
		for email in beta_emails_array:
			msg = prepMail("Activation Code for Muscle Tracker App", email)

			try:
				print("Attempting to send message")
				msg.send()
			except Exception as e:
				print("Unable to send mail")
				print(e)

		rtn_dict['success'] = True
	except Exception as e:
		print 'Error sending beta app emails out: {0}'.format(e)

	return HttpResponse(json.dumps(rtn_dict, cls=DjangoJSONEncoder), content_type="application/json")