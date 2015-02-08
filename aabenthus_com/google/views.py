from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.core.urlresolvers import reverse

import json
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.django_orm import Storage
from aabenthus_com.google import services

from .models import Authorization

def authorize(request):
	redirect_uri = request.build_absolute_uri( reverse('oauth2callback') )
	flow = OAuth2WebServerFlow(settings.GOOGLE_CLIENT_ID,
                             settings.GOOGLE_CLIENT_SECRET,
                             settings.GOOGLE_SCOPE,
                             redirect_uri=redirect_uri,
                             access_type='offline' )
	authorize_url = flow.step1_get_authorize_url()

	return redirect(authorize_url)

def oauth2callback(request):
	redirect_uri = request.build_absolute_uri( reverse('oauth2callback') )
	flow = OAuth2WebServerFlow(settings.GOOGLE_CLIENT_ID,
                             settings.GOOGLE_CLIENT_SECRET,
                             settings.GOOGLE_SCOPE,
                             redirect_uri=redirect_uri,
                             access_type='offline' )
	code = request.GET['code']
	credentials = flow.step2_exchange(code)
	
	oauth2 = services.oauth2(credentials)
	userinfo_request = oauth2.userinfo().get()
	userinfo = userinfo_request.execute()

	storage = Storage(Authorization, 'email', userinfo.get('email'), 'credentials')
	storage.put(credentials)

	response = {'status': 'ok'}
	return HttpResponse( json.dumps(response),
		content_type="application/json" )