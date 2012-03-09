from django.conf.urls.defaults import url, patterns
from bandbook.instruments.views import *
from bandbook.urls import SLUG_REGEX

urlpatterns = patterns('bandbook.instruments.views',
    # "normal" urls here...
)

urlpatterns += patterns('bandbook.instruments.views',
    *InstrumentTypeView.urls('list/(?P<slug>[a-z0-9-_]+)/types',
        ['create', 'update', 'delete', 'order'])
)

urlpatterns += patterns('bandbook.instruments.views',
    *InstrumentCategoryView.urls('list',
        ['list', 'create', 'update', 'delete', 'order'], uregex=SLUG_REGEX)
)

urlpatterns += patterns('bandbook.instruments.views',
    *InstrumentModelView.urls('manufacturers/(?P<slug>[a-z0-9-_]+)/models',
        ['create', 'update', 'delete'])
)

urlpatterns += patterns('bandbook.instruments.views',
    *InstrumentManufacturerView.urls('manufacturers',
        ['list', 'create', 'update', 'delete'], uregex=SLUG_REGEX)
)

urlpatterns += patterns('bandbook.instruments.views',
    *InstrumentHistoryView.urls('(?P<slug>[a-z0-9-_]+)/history',
        ['create', 'update', 'delete', 'print'])
)

urlpatterns += patterns('bandbook.instruments.views',
    *InstrumentView.urls('',
        ['list', 'create', 'detail', 'update', 'delete'], uregex=SLUG_REGEX)
)
