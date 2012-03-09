from django.utils.translation import ugettext_lazy as _


def dummy_for_makemessages():
    """
    This function allows manage makemessages to find the forecast types
    for translation. Removing this code causes makemessages to comment out
    those PO entries, so don't do that unless you find a better way to do this
    """
    _('Owned')
