import os
import sys
sys.path = ['/home/akira/git/SGC/SGC/'] + sys.path
os.environ['DJANGO_SETTINGS_MODULE'] = 'SGC.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
