from bandbook.main.views import BBView
from bandbook.instruments.forms import InstrumentForm, InstrumentHistoryForm, \
    InstrumentCategoryForm, InstrumentTypeForm
from bandbook.instruments.models import Instrument, InstrumentCategory, \
    InstrumentManufacturer, InstrumentType, InstrumentModel, InstrumentHistory


class InstrumentView(BBView):
    model = Instrument
    form_class = InstrumentForm


class InstrumentHistoryView(BBView):
    model = InstrumentHistory
    form_class = InstrumentHistoryForm
    parent = {'field': 'instrument', 'param': 'slug',
              'model': Instrument}


class InstrumentCategoryView(BBView):
    model = InstrumentCategory
    form_class = InstrumentCategoryForm


class InstrumentTypeView(BBView):
    model = InstrumentType
    form_class = InstrumentTypeForm
    parent = {'field': 'category', 'param': 'slug',
              'model': InstrumentCategory}


class InstrumentManufacturerView(BBView):
    model = InstrumentManufacturer


class InstrumentModelView(BBView):
    model = InstrumentModel
    parent = {'field': 'manufacturer', 'param': 'slug',
              'model': InstrumentManufacturer}
