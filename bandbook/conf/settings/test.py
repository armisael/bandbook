import default

INSTALLED_APPS = default.INSTALLED_APPS + (
    'devdata',
    'pagination',
)

DISABLED_APPS = default.DISABLED_APPS + (
    'sentry', 'sentry.client', 'sentry.plugins.sentry_urls',
    'south'
)

DEBUG = False
COMPRESS_ENABLED = True
