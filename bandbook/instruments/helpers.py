from django.contrib.contenttypes.models import ContentType
from django.db.models.aggregates import Max


def get_default_ordering(cls, parent_id=None):
    try:
        filters = {}
        if parent_id is not None and hasattr(cls, 'parent_model'):
            parent_field = '%s' % cls.parent_model[0]
            filters[parent_field] = parent_id
        return cls._default_manager.filter(**filters).\
                    aggregate(Max('ordering')).values()[0] + 1
    except TypeError:  # empty queryset
        return 1


#def get_default_ordering(app_name, model_name):
#
#    def compute_ordering():
#        c_type = ContentType.objects.get(app_label=app_name, model=model_name)
#        cls = c_type.model_class()
#        return get_default_ordering(cls)
#
#    return compute_ordering
#
