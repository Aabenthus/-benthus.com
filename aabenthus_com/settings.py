# -*- coding: utf-8 -*-
"""
Django settings for aabenthus_com project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'dont-even-bother'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = [
	'local.api.xn--benthus-dxa.com',
	'api.xn--benthus-dxa.com'
]


# Application definition

INSTALLED_APPS = (
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'corsheaders',

	'aabenthus_com.google',
	'aabenthus_com.rooms'
)

MIDDLEWARE_CLASSES = (
	'django.contrib.sessions.middleware.SessionMiddleware',
	'corsheaders.middleware.CorsMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'aabenthus_com.urls'

WSGI_APPLICATION = 'aabenthus_com.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	}
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

#TIME_ZONE = 'UTC'
TIME_ZONE = 'Europe/Copenhagen'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

CORS_ORIGIN_WHITELIST = (
	'rooms.airtame.com',
	'rooms.socialsquare.dk',
	'local.xn--benthus-dxa.com',
	'xn--benthus-dxa.com',
	'local.www.xn--benthus-dxa.com',
	'www.xn--benthus-dxa.com'
)

GOOGLE_CLIENT_ID = '1067303134515-23n0icstkai0gi5uf5t7ocld1phgor4a.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = 'set-this-in-a-local-settings-file'
GOOGLE_SCOPE = (
	'https://www.googleapis.com/auth/calendar',
	'https://www.googleapis.com/auth/userinfo.email',
	'https://www.googleapis.com/auth/userinfo.profile'
)

ROOMS_EMAIL = 'rooms@xn--benthus-dxa.com'

CONFLICT_MAIL_SUBJECT = 'Room booking rejected: %s'
CONFLICT_MAIL_FROM = ROOMS_EMAIL

FRONTEND_BASE_URL = 'http://åbenthus.com'
