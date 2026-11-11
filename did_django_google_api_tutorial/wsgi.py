

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'did_django_google_api_tutorial.settings')

application = get_wsgi_application()
