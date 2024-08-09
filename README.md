# WonderFell_Media
Media server running on Flask, using Apache2, MySQL, WSGI, Bootstrap, DJango, & Jinja to authenticate and post music + cover art in table environment.

Key directories must be updated in __init__.py within "app" folder to set credentials for MySQL DB + routes.py within "app" folder to set Authentication Key for hashing credentials in DB.

To use as standalone, install mysql and Apache2.

For configuration of Apache2, include the lines:

ServerAdmin email.com
ServerName localhost
DocumentRoot /path/to/root

For use with WSGI, install install python3 virtualenv module using PIP. Create a virtual environment named WSGI and install all packages using bash requirements.sh. For configuration of Apache2 for use with WSGI, include the lines:

WSGIDaemonProcess wsgi python-home= /path/to/virtual/environment
WSGIProcessGroup wsgi
WSGIApplicationGroup %{GLOBAL}
WSGIScriptAlias / /path/to/root/yourapplication.wsgi