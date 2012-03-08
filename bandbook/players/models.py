from django.db import models
from django_extensions.db.fields import AutoSlugField
from django_extensions.db.models import TimeStampedModel
from bandbook.instruments.models import InstrumentType


class Player(TimeStampedModel):
    name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    birthdate = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=16, blank=True, null=True)
    mobile_number = models.CharField(max_length=16, blank=True, null=True)
    picture = models.ImageField(blank=True, null=True, upload_to='pictures/')
    slug = AutoSlugField('slug', populate_from=('name', 'surname'),
                         unique=True, editable=False)

    instrument_type = models.ForeignKey(InstrumentType)

    def full_name(self):
        return '%s %s' % (self.name, self.surname)

    def __unicode__(self):
        return '%s (%s)' % (self.full_name(), self.instrument_type)
