import json
from django.contrib.auth.models import User

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse

from django.core.mail import send_mail, EmailMessage

def signup(request):
	return render_to_response('signup.html', {}, context_instance=RequestContext(request))