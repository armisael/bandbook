from test import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'bandbook',              # Or path to database file if using sqlite3.
        'USER': 'postgres',              # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '127.0.0.1',             # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',                  # Set to empty string for default. Not used with sqlite3.
    }
}
