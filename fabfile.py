# a test
from __future__ import with_statement

import os
from fabric.api import *
from fabric.operations import _shell_escape
from fabric.contrib import files

#env.web_root = "/home/web"
#env.project_name = "moka"
#env.compass_bin = "/var/lib/gems/1.8/bin/compass"
#env.venv_root = '/home/web/Envs'
#env.venv_name = 'moka'
#env.our_user = 'web'
#env.our_group = 'web'
#env.repo = 'gitolite@git.ahref.eu:moka'
#env.debug = False
#env.branch_name = 'master'
#env.use_shell = False
#cucu

def update_translations():
    """
    Update *.po in the LOCAL repository
    """
    local("python manage.py makemessages -e html -e email -e txt -l it")
    # local("python manage.py makemessages -d djangojs -i '*CACHE*' -l it")
