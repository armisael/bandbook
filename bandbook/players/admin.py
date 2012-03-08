import reversion

from django.contrib import admin
from bandbook.players.models import Player


class PlayerAdmin(reversion.VersionAdmin):
    list_display = ['name', 'surname', 'instrument_type']
    list_select_related = True

    def instrument_type_count(self, obj):
        return obj.instrumenttype_set.count()


admin.site.register(Player, PlayerAdmin)
