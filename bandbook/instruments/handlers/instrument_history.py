from django.utils.translation import ugettext as _


class InstrumentHistoryBase(object):
    id = -1
    name = u''
    description = u''
    with_player = False

    def __init__(self):
        assert(self.id >= 0)
        assert(len(self.name) > 0)
        assert(len(self.description) > 0)

    def get_description(self, instrument_history):
        if self.with_player and instrument_history.target:
            return self.description % {
                'player': instrument_history.target,
            }
        else:
            return self.description

    def __unicode__(self):
        return self.name


class Booking(InstrumentHistoryBase):
    id = 1
    name = _('Booking')
    description = _('Booked by %(player)s')
    with_player = True


class Repair(InstrumentHistoryBase):
    id = 2
    name = _('In Repair')
    description = _('In Repair')
    with_player = False


class InstrumentHistorySite(object):
    _registry = {}
    _choices = []

    def __init__(self, a_list):
        for x in a_list:
            self._registry[x.id] = x
            self._choices.append((x.id, x.name))

    def get_by_id(self, id):
        return self._registry.get(int(id))

    def choices(self):
        return self._choices


site = InstrumentHistorySite((Booking, Repair, ))
