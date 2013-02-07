# Django settings for pipeye project.
import os
from django.core.urlresolvers import reverse_lazy

# Path to root of Python code
CODE_ROOT = os.path.dirname(os.path.dirname(__file__))

# Path to project root
ROOT = os.path.dirname(CODE_ROOT)

def project_path(*segments):
    """Generate path relative to project root"""
    return os.path.join(ROOT, *segments)

ADMINS = MANAGERS = (
    ('Tomek Paczkowski', 'tomek@hauru.eu'),
)

# i18n settings
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True

# Timezone settings
TIME_ZONE = 'UTC'
USE_TZ = True

# User uploaded media
MEDIA_ROOT = ''
MEDIA_URL = ''

# Path where collectstatic puts all files
STATIC_ROOT = project_path('public')

# URL to where static files are hosted
STATIC_URL = '/static/'

# Path to project-wide static files
STATICFILES_DIRS = (
    project_path('static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = (
    project_path('templates'),
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'pipeye.urls'
WSGI_APPLICATION = 'pipeye.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'south',
    'gunicorn',
    'compressor',
    'social_auth',
    'pipeye.packages',
    'pipeye.watches',
)

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.contrib.github.GithubBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# compressor settings
COMPRESS_PRECOMPILERS = (
    ('text/coffeescript', 'coffee --compile --stdio'),
    ('text/x-sass', 'sass {infile} {outfile}'),
)

# social-auth settings
LOGIN_URL = reverse_lazy('login')
LOGIN_REDIRECT_URL = reverse_lazy('home')
SOCIAL_AUTH_COMPLETE_URL_NAME = 'login_complete'


# Testing settings
TEST_RUNNER = 'discover_runner.DiscoverRunner'
TEST_DISCOVER_TOP_LEVEL = ROOT

# A sample logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
