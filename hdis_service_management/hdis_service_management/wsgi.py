"""
WSGI config for hdis_service_management project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from static_variables import *

os.environ.setdefault("DJANGO_SETTINGS_MODULE", setting_file)
application = get_wsgi_application()
