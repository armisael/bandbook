from django.forms.widgets import DateInput


class BootstrapDatepicker(DateInput):
    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}
        if 'class' not in attrs:
            attrs['class'] = ''
        attrs['class'] += ' datepicker'
        return super(BootstrapDatepicker, self).render(name, value, attrs)
