import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path = [BASE_DIR] + sys.path
os.environ['DJANGO_SETTINGS_MODULE'] = 'SGC.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
