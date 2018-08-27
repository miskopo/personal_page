#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/FirstOfficersLog/")

from FirstOfficersLog import app as application
application.secret_key = 'H4B5E6R7F8V9D5'
