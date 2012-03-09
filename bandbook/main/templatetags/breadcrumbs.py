from django.core.urlresolvers import reverse, NoReverseMatch
from django.template.defaultfilters import register
from django.utils.translation import ugettext as _
from templatetag_sugar.parser import Variable, Constant
from templatetag_sugar.register import tag


@tag(register, [])
def breadcrumb_open(context):
    return """<ul class="breadcrumb"> %s""" % \
           breadcrumb_entry(context, "", "index", icon='home')


@tag(register, [Variable(), Constant("to"), Variable()])
def breadcrumb_entry(context, title, url_name, last=False, icon=None):
    try:
        url = reverse(url_name)
    except NoReverseMatch:
        url = ''
    return """
    <li class="%(class)s">
       <a href="%(url)s">%(icon)s %(title)s</a> %(divider)s
    </li>""" % {
        'title': _(title) if title else "",
        'url': url,
        'class': 'active' if last else '',
        'divider': ' <span class="divider">/</span>' if not last else '',
        'icon': '<i class="icon-%s"></i>' % icon if icon else '',
    }


@tag(register, [Variable()])
def breadcrumb_close(context, title):
#    return '%s </ul>' % breadcrumb_entry(context, title, '', last=True)
    return '</ul>'
