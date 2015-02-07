from apiclient.discovery import build
import httplib2
from oauth2client.client import OAuth2Credentials

def oauth2(authorization):
	assert(authorization != None, 'The authorization parameter cant be None')
	credentials = OAuth2Credentials.from_json( authorization.credentials )
	http = httplib2.Http()
	http = credentials.authorize(http)
	service = build('oauth2', 'v2', http=http)
	return service

def calendar(authorization):
	assert(authorization != None, 'The authorization parameter cant be None')
	credentials = OAuth2Credentials.from_json( authorization.credentials )
	http = httplib2.Http()
	http = credentials.authorize(http)
	service = build('calendar', 'v3', http=http)
	return service