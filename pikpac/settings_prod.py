try:
    from .settings_shared import *
except ImportError:
    pass


DEBUG = False

ALLOWED_HOSTS = ['thinksmall.lionking.org']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASS'],
        'HOST': os.environ['DB_HOST'],
        'PORT': os.environ['DB_PORT'],
        'OPTIONS': {
            'init_command': 'SET character_set_connection=utf8mb4, collation_connection=utf8mb4_general_ci',
            'charset': 'utf8mb4',
        },
    },
}

STATIC_ROOT = '/usr/local/www/django/thinksmall/static_root'
MEDIA_ROOT = '/usr/local/www/django/thinksmall/media'

EMAIL_HOST = 'mail.lionking.org'

SITE_EMAIL = 'fanart@lionking.org'
DEBUG_EMAIL = 'btman@mac.com'
ADMIN_EMAIL = 'btman@lionking.org'

ADMINS = [(ADMIN_NAME, DEBUG_EMAIL)]

RECAPTCHA_ENABLED = True

CELERY_BROKER_URL = os.environ['CELERY_BROKER_URL']

