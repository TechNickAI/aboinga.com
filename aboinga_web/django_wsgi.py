import os
import sys

# Virtualenv. See http://code.google.com/p/modwsgi/wiki/VirtualEnvironments
import site
site.addsitedir('/var/www/aboinga.com/aboingaenv/lib/python2.6/site-packages')

# Add the current dir to path
sys.path.append(os.path.dirname(__file__))
# adnd the grandparent
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
os.environ['ABOINGA_ENVIRONMENT'] = 'prod'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
