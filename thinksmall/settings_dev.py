try:
    from .settings_shared import *
except ImportError:
    pass


DEBUG = True

ALLOWED_HOSTS = ['localhost']

STATIC_ROOT = '/Users/brian.tiemann/Development/thinksmall/static_root'

MEDIA_ROOT = '/Users/brian.tiemann/Development/thinksmall/media'

CELERY_TASK_ALWAYS_EAGER = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SITE_EMAIL = 'info@thinksmall.com'
DEBUG_EMAIL = 'btman@mac.com'
ADMIN_EMAIL = 'btman@mac.com'

