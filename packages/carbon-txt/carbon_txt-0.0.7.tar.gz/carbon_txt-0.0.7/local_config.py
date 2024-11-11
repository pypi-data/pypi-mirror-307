from carbon_txt.web.config.settings.base import *  # noqa

DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost", ".localhost"]

WSGI_APPLICATION = "carbon_txt.web.config.wsgi.application"
ROOT_URLCONF = "carbon_txt.web.config.urls"

# Allow connections from any 'local' domain, like
# if you are using '.dev' or '.local' domain with a reverse proxy
# like Caddy or Nginx
CORS_ALLOW_ALL_ORIGINS = True
