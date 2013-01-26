# pipeye production settings
from .base import *
from django.core.exceptions import ImproperlyConfigured
import os
import dj_database_url

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': dj_database_url.config(env='DATABASE_URL')
}

SECRET_KEY = os.environ.get('SECRET_KEY')

try:
    GITHUB_APP_ID = os.environ['GITHUB_APP_ID']
    GITHUB_API_SECRET = os.environ['GITHUB_API_SECRET']
except KeyError:
    raise ImproperlyConfigured('Please provide GitHub app credentials')
