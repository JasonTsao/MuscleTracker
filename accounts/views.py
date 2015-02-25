import json
from django.contrib.auth.models import User

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse

from django.core.mail import send_mail, EmailMessage

from forms import BetaEmailForm

def signup(request):
	return render_to_response('email/submit_email.html', {"form":BetaEmailForm()}, context_instance=RequestContext(request))