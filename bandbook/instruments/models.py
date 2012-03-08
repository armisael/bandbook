from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db.models.query_utils import Q
from django.template.defaultfilters import date as _date
from django.utils.translation import ugettext as _
from django.db import models
from django_extensions.db.fields import AutoSlugField
from django_extensions.db.models import TimeStampedModel

from bandbook.instruments.handlers.instrument_history import site


class InstrumentCategory(TimeStampedModel):
    name = models.CharField(max_length=64, verbose_name=_("Name"),)
    ordering = models.IntegerField(editable=False,
           default=-1, verbose_name=_("Ordering"))
    slug = AutoSlugField('slug', populate_from='name',
                         unique=True, editable=False)

    search_by = ('name', 'instrumenttype__name')
    class Meta:
        ordering = ['ordering']
        verbose_name_plural = "Instrument categories"

    def __unicode__(self):
        return self.name


class InstrumentType(TimeStampedModel):
    name = models.CharField(max_length=64, verbose_name=_("Name"))
    category = models.ForeignKey(InstrumentCategory, verbose_name=_("Category"))
    ordering = models.IntegerField(editable=False,
               default=-1, verbose_name=_("Ordering"))
    slug = AutoSlugField('slug', populate_from='name',
                         unique=True, editable=False)

    parent_model = ('category', InstrumentCategory)
    class Meta:
        ordering = ['ordering']

    def __unicode__(self):
        return u"%s" % (self.name, )


class InstrumentManufacturer(TimeStampedModel):
    name = models.CharField(max_length=64, verbose_name=_("Name"))
    slug = AutoSlugField('slug', populate_from='name',
                         unique=True, editable=False)

    search_by = ('name', 'instrumentmodel__name', 'instrumentmodel__type__name',
                 'instrumentmodel__type__category__name')
    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class InstrumentModel(TimeStampedModel):
    name = models.CharField(max_length=64, verbose_name=_("Name"))
    type = models.ForeignKey(InstrumentType, verbose_name=_("Type"))
    manufacturer = models.ForeignKey(InstrumentManufacturer,
                                     verbose_name=_("Manufacturer"))
    slug = AutoSlugField('slug', populate_from='name',
                         unique=True, editable=False)

    parent_model = ('manufacturer', InstrumentManufacturer)
    class Meta:
        ordering = ['type__ordering']

    def __unicode__(self):
        return u'%s %s - %s' % (self.type, self.manufacturer, self.name)


class Instrument(TimeStampedModel):
    model = models.ForeignKey(InstrumentModel, verbose_name=_("Model"))
    date_of_purchase = models.DateField(verbose_name=_("Date of Purchase"))
    code = models.CharField(max_length=64, verbose_name=_("Code"))
    slug = AutoSlugField('slug', populate_from='code',
                         unique=True, editable=False)

    search_by = ('code', 'model__name', 'model__manufacturer__name',
                 'model__type__name', 'model__type__category__name', )
    class Meta:
        ordering = ['model__type__ordering']

    def __unicode__(self):
        return u'%s - %s' % (self.model, self.code)

    def get_status(self):
        try:
            return self.instrumenthistory_set.filter(date_end=None)[0]
        except IndexError:
            return _('---')

    def get_condition(self):
        try:
            return self.instrumenthistory_set.filter(~Q(condition=None) &
                                                     ~Q(condition=''))[0].condition
        except IndexError:
            return _('---')

    def get_absolute_url(self):
        return reverse('instrument_detail', args=(self.slug, ))


    # TODO stampa modulo di prestito
class InstrumentHistory(TimeStampedModel):
    instrument = models.ForeignKey(Instrument, verbose_name=_("Instrument"))
    date_start = models.DateField(verbose_name=_("From"))
    date_end = models.DateField(blank=True, null=True, verbose_name=_("To"))
    event_id = models.IntegerField(verbose_name=_("Event"))
    condition = models.TextField(blank=True, default='', verbose_name=_("Condition"))
    notes = models.TextField(blank=True, default='', verbose_name=_("Notes"))
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)

    target = GenericForeignKey('content_type', 'object_id')

    parent_model = ('instrument', Instrument)
    class Meta:
        ordering = ['-date_start']

    def get_event(self):
        return site.get_by_id(self.event_id)

    def __unicode__(self):
        try:
            return _('%(description)s since %(date_start)s') % {
                'description': self.get_event()().get_description(self),
                'date_start': _date(self.date_start, 'd F Y'),
                }
        except TypeError:
            return _('error')
