"""
WSGI config for pikpac project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os, sys
from django.core.wsgi import get_wsgi_application

env_variables_to_pass = [
    'BASE_PATH',
    'SECRET_KEY',
    'DJANGO_SETTINGS_MODULE',
]

def application(environ, start_response):
    # pass the WSGI environment variables on through to os.environ
    for var in env_variables_to_pass:
        os.environ[var] = environ.get(var, '')
    sys.path.append(os.environ['BASE_PATH'])
    return get_wsgi_application()(environ, start_response)

