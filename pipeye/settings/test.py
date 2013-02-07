# pipeye settings for speed testing
from .base import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

# Using sqlite for it's in-memory storage
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'pipeye.sqlite'
    }
}

# No migrations needed in tests
SOUTH_TESTS_MIGRATE = False

# Use fast hashers
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
)

GITHUB_APP_ID = 'app_id'
GITHUB_API_SECRET = 'api_secret'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'WARNING',
        },
    }
}
