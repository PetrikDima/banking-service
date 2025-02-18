# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
import os
from urllib.parse import urlparse

from back_end.utils.settings import BASE_DIR

# USE_SQLITE = os.getenv("USE_SQLITE", "False") == "True"
USE_SQLITE = True

if USE_SQLITE:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    tmpPostgres = urlparse(os.getenv("DATABASE_URL"))
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': tmpPostgres.path.replace('/', ''),
            'USER': tmpPostgres.username,
            'PASSWORD': tmpPostgres.password,
            'HOST': tmpPostgres.hostname,
            'PORT': 5432,
        }
    }
