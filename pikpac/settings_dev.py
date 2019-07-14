try:
    from .settings_shared import *
except ImportError:
    pass


DEBUG = True

ALLOWED_HOSTS = ['localhost', 'api.pikpac.grotto11.com']

STATIC_ROOT = '/Users/brian.tiemann/Development/pikpac/static_root'

MEDIA_ROOT = '/Users/brian.tiemann/Development/pikpac/media'

CELERY_TASK_ALWAYS_EAGER = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SITE_EMAIL = 'info@pikpac.com'
DEBUG_EMAIL = 'btman@mac.com'
ADMIN_EMAIL = 'btman@mac.com'

