from apiclient.discovery import build
import httplib2
from oauth2client.client import OAuth2Credentials

def oauth2(credentials):
	http = httplib2.Http()
	http = credentials.authorize(http)
	service = build('oauth2', 'v2', http=http)
	return service

def calendar(credentials):
	http = httplib2.Http()
	http = credentials.authorize(http)
	service = build('calendar', 'v3', http=http)
	return service