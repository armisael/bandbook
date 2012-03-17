import re
from uuid import uuid4
from datetime import date

from django.template.defaultfilters import register
from django.utils.safestring import mark_safe
from bandbook.main.helpers import index_block, filter_queryset, \
    filter_searchby, filter_matches


@register.inclusion_tag('logo.html')
def logo():
    blocks = [
            index_block(16, 16, 18, 'nw', style='error'),
            index_block(16, 16, 15, 'ne', style='warning'),
            index_block(16, 16, 12, 'se', style='info'),
            index_block(16, 16, 9, 'sw', style='success'),
            ]
    return {'blocks': blocks}


def render_table(request, obj_list, header, fields, actions, parent_pk=None,
                 is_subtable=False, subtable=None, prefix=''):

    if len(obj_list) and hasattr(obj_list[0], 'get_absolute_url'):
        actions.append('view')

    return {
        'request': request,
        'obj_list': obj_list,
        'header': header,
        'fields': fields,
        'new': 'new' in actions,
        'edit': 'edit' in actions,
        'delete': 'del' in actions,
        'drag': 'drag' in actions,
        'view': 'view' in actions,
        'pdf': 'pdf' in actions,
        'has_actions': len(actions),
        'is_subtable': is_subtable,
        'subtable': subtable,
        'prefix': prefix,
        'parent_pk': parent_pk,
        'uid': uuid4(),
    }


@register.inclusion_tag('widgets/table.html', takes_context=True)
def render_subtable(context, obj, config):
    query_set_field = config.get('query_set')
    if not hasattr(obj, query_set_field):
        return

    query_set = getattr(obj, query_set_field).all()

    request = context['request']
    query = request.GET.get('q')
    if query and hasattr(obj, 'search_by'):
        parent_search_by, children_search_by = \
                filter_searchby(getattr(obj, 'search_by'), query_set_field)
        # if `obj' matches the query, we want to show the entire query_set,
        # otherwise we want to filter it as well.
        if not filter_matches(obj, query, parent_search_by):
            query_set = filter_queryset(query_set, query, children_search_by)

    prefix = config.get('prefix', '')
    params = {}
    for attr in re.findall('%\((?P<attr>[a-zA-Z]+)\)s', prefix):
        params[attr] = getattr(obj, attr)
    prefix = prefix % params

    return render_table(
        request,
        query_set,
        header=config.get('header', []),
        fields=config.get('fields', []),
        actions=config.get('actions', []),
        prefix=prefix,
        parent_pk=obj.pk,
        is_subtable=True,
    )


@register.inclusion_tag('widgets/form.html')
def render_form(form):
    return {
        'form': form,
        'uid': uuid4(),
    }


@register.filter()
def get_attrib(obj, attr):
    attrs = attr.split('.')
    for attr in attrs:
        if not hasattr(obj, attr):
            return None
        obj = getattr(obj, attr)
        if hasattr(obj, '__call__'):
            obj = obj()
    return obj


@register.filter()
def is_dictionary(obj):
    return isinstance(obj, dict)


@register.filter()
def add_one_if(curr_value, condition):
    return curr_value + 1 if condition else curr_value


@register.filter()
def get_absolute_url(obj, prefix):
    """ Returns the base url of the given object, using prefix if needed.
    """
    try:
        return obj.get_absolute_url()
    except AttributeError:
        if not hasattr(obj, 'parent_model') and hasattr(obj, 'slug'):
            return '%s%s/' % (prefix, obj.slug)
        return '%s%d/' % (prefix, obj.pk)


@register.filter()
def real_spaces(str):
    return mark_safe(str.replace(' ', '&nbsp;'))


@register.filter()
def today(str):
    return date.today()


@register.filter()
def get(dictionary, key):
    return dictionary.get(key)


@register.filter()
def to_left(obj, length):
    str = unicode(obj)
    return " " + str + " " * (length - len(str) - 1)
