from django.template.defaultfilters import register
from django.utils.translation import ugettext as _
from bandbook.main.templatetags.bandbook_main import render_table


@register.inclusion_tag('widgets/table.html', takes_context=True)
def render_instruments_table(context, instruments):
    request = context['request']
    user = request.user

    return render_table(
        request,
        instruments,
        header=[_('Model'), _('Date of Purchase'), _('Code'), _('Status')],
        fields=['model', 'date_of_purchase', 'code', 'get_status'],
        actions=['edit', 'del', 'new'] if user.is_staff else []
    )


@register.inclusion_tag('widgets/table.html', takes_context=True)
def render_instrumentcategory_table(context, categories):
    request = context['request']
    user = request.user

    return render_table(
        request,
        categories,
        header=[_('Category'), _("Instrument")],
        fields=['name', {
            'prefix': '%(slug)s/types/',
            'query_set': 'instrumenttype_set',
            'header': [_('Name')],
            'fields': ['name'],
            'actions': ['drag', 'edit', 'del', 'new'] if user.is_staff else [],
        }],
        actions=['drag', 'edit', 'del', 'new'] if user.is_staff else [],
    )


@register.inclusion_tag('widgets/table.html', takes_context=True)
def render_instrumentmanufacturers_table(context, manufacturers):
    request = context['request']
    user = request.user

    return render_table(
        request,
        manufacturers,
        header=[_('Name'), _('Models')],
        fields=['name', {
            'prefix': '%(slug)s/models/',
            'query_set': 'instrumentmodel_set',
            'header': [_('Name'), _('Type')],
            'fields': ['name', 'type'],
            'actions': ['edit', 'del', 'new'] if user.is_staff else [],
        }],
        actions=['edit', 'del', 'new'] if user.is_staff else [],
    )


@register.inclusion_tag('widgets/table.html', takes_context=True)
def render_instrumenthistory_table(context, obj, history):
    request = context['request']
    user = request.user
    return render_table(
        request,
        history,
        header=[_('Event'), _('From'), _('To'), _('Player')],
        fields=['get_event.name', 'date_start', 'date_end', 'target'],
        actions=['pdf', 'edit', 'del', 'new'] if user.is_staff else [],
        prefix='%shistory/' % obj.get_absolute_url(),
    )
