import sys

## Import our defaults (globals)
from conf.settings.default import *

## Inherit from environment specifics

sys.path.append(PROJECT_PATH)
DJANGO_CONF = os.environ.get('DJANGO_CONF', 'default')
if DJANGO_CONF != 'default':
    module = __import__('conf.settings.' + DJANGO_CONF,
                        globals(), locals(), ['*'])
    for k in dir(module):
        if k.startswith('__'):
            continue
        locals()[k] = getattr(module, k)
sys.path.pop()

## Import local settings
try:
    from settings_local import *
except ImportError:
    pass
