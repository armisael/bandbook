import reversion

from django.contrib import admin
from bandbook.instruments.models import InstrumentCategory, Instrument, \
    InstrumentType, InstrumentManufacturer, InstrumentModel, InstrumentHistory


class InstrumentCategoryAdmin(reversion.VersionAdmin):
    list_display = ['name', 'ordering', 'instrument_type_count']
    list_select_related = True

    def instrument_type_count(self, obj):
        return obj.instrumenttype_set.count()


class InstrumentTypeAdmin(reversion.VersionAdmin):
    list_display = ['name', 'category', 'ordering']


class InstrumentManufacturerAdmin(reversion.VersionAdmin):
    list_display = ['name']


class InstrumentModelAdmin(reversion.VersionAdmin):
    list_display = ['name', 'type', 'manufacturer', 'instrument_count']

    def instrument_count(self, obj):
        return obj.instrument_set.count()


class InstrumentAdmin(reversion.VersionAdmin):
    list_display = ['model', 'date_of_purchase', 'code']


class InstrumentHistoryAdmin(reversion.VersionAdmin):
    list_display = ['instrument', 'get_event', 'date_start',
                    'date_end', 'target']


admin.site.register(InstrumentCategory, InstrumentCategoryAdmin)
admin.site.register(InstrumentType, InstrumentTypeAdmin)
admin.site.register(InstrumentManufacturer, InstrumentManufacturerAdmin)
admin.site.register(InstrumentModel, InstrumentModelAdmin)
admin.site.register(Instrument, InstrumentAdmin)
admin.site.register(InstrumentHistory, InstrumentHistoryAdmin)
