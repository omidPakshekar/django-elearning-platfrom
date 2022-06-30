import os


from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_CONFIGURATION", "Prod")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_elearning.settings')

from configurations.wsgi import get_wsgi_application

application = get_wsgi_application()
