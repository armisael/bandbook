from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.forms.models import ModelForm
from django.forms.widgets import HiddenInput, Textarea
from django.forms import ModelChoiceField, ChoiceField
from bandbook.instruments.helpers import get_default_ordering
from bandbook.instruments.models import Instrument, InstrumentHistory, InstrumentCategory, InstrumentType
from bandbook.instruments.handlers.instrument_history import site
from bandbook.main.widgets import BootstrapDatepicker
from bandbook.players.models import Player


class InstrumentForm(ModelForm):
    class Meta:
        model = Instrument
        widgets = {
            'date_of_purchase': BootstrapDatepicker(),
        }


class InstrumentCategoryForm(ModelForm):
    class Meta:
        model = InstrumentCategory

    def clean_ordering(self):
        ordering = self.cleaned_data.get('ordering')
        if ordering <= 0:  # default value (new model instance)
            ordering = get_default_ordering(InstrumentCategory)
        return ordering


class InstrumentTypeForm(ModelForm):
    class Meta:
        model = InstrumentType

    def clean_ordering(self):
        ordering = self.cleaned_data.get('ordering')
        category = self.cleaned_data.get('category_id')
        if ordering <= 0:  # default value (new model instance)
            ordering = get_default_ordering(InstrumentType, category)
        return ordering


class InstrumentHistoryForm(ModelForm):
    player = ModelChoiceField(queryset=Player.objects.all(), required=False,
                              label=_("Player"))
    event_id = ChoiceField(choices=site.choices(), label=_('Event'))

    class Meta:
        model = InstrumentHistory
        fields = ('instrument', 'event_id', 'date_start', 'date_end',
                  'player', 'content_type', 'object_id', 'condition', 'notes')
        widgets = {
            'date_start': BootstrapDatepicker(),
            'date_end': BootstrapDatepicker(),
            'instrument': HiddenInput(),
            'content_type': HiddenInput(),
            'object_id': HiddenInput(),
            'condition': Textarea(attrs={'rows':2, 'class': 'span4'}),
            'notes': Textarea(attrs={'rows':2, 'class': 'span4'}),
        }

    def __init__(self, *args, **kwargs):
        if 'instance' in kwargs and kwargs['instance'] is not None:
            kwargs['initial']['player'] = kwargs['instance'].target
        super(InstrumentHistoryForm, self).__init__(*args, **kwargs)

    def clean_player(self):
        player = self.cleaned_data.get('player')
        action = site.get_by_id(self.cleaned_data['event_id'])
        if action.with_player and player is None:
            raise ValidationError(
                _('This field is required with the specified event'))
        return player

    def clean(self):
        super(InstrumentHistoryForm, self).clean()
        player = self.cleaned_data.get('player')

        if player is not None:
            c_type = ContentType.objects.get_for_model(Player)
            self.cleaned_data['content_type'] = c_type
            self.cleaned_data['object_id'] = player.pk

        return self.cleaned_data
