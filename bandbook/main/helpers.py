from random import randint
from django.test import TestCase
from django.contrib.auth.models import User
from django.db.models.query_utils import Q

from django.utils.functional import lazy
from django.core.urlresolvers import reverse


reverse_lazy = lazy(reverse, str)


def index_block(x, y, width, gravity, style=None, url=None,
                img_class=None, tmpl_class=None):
    padding = 4
    images = {'scores': ['/static/images/photos/scores1.png',
                         '/static/images/photos/scores2.png',
                         '/static/images/photos/scores3.png',
                         ],
              'instruments': ['/static/images/photos/instruments1.png',
                              '/static/images/photos/instruments2.png',
                              '/static/images/photos/instruments3.png',
              ],
              'players': ['/static/images/photos/players1.png',
                          '/static/images/photos/players2.png',
                          '/static/images/photos/players3.png',
                          ],
              }
    img_url = None
    if img_class:
        img_list = images.get(img_class)
        if img_list:
            img_url = img_list[randint(0, len(img_list) - 1)]

    if gravity[0] == 'n':
        y -= (width + padding)
    if gravity[1] == 'w':
        x -= (width + padding)
    return x, y, width, width, style, url, img_url, tmpl_class


def filter_queryset(sqs, query, search_by):
    if len(search_by):
        filters = None
        for attr in search_by:
            params = dict((('%s__icontains' % attr, query),))
            if filters is None:
                filters = Q(**params)
            else:
                filters |= Q(**params)
        # in case of filtering on sub-classes, need to remove
        # duplicates
        return sqs.filter(filters).distinct()
    return sqs


def filter_searchby(parent_searchby, parent_field_set):
    """ Given the search_by field of a parent class, and the name of
        its field for the children query-set, it returns two lists: the
        fields of search-by that are actually about the parent, and the ones
        that are for children.
    """
    key = parent_field_set[:-4]
    set_children = [x for x in parent_searchby if x.find(key) != -1]
    set_parent = [x for x in parent_searchby if x not in set_children]
    return set_parent, [x[len(key) + 2:] for x in set_children]


def filter_matches(obj, query, filters):
    """ Tests whether `obj' matches `filters'
    """
    return filter_queryset(obj.__class__.objects.filter(pk=obj.pk),
                           query,
                           filters).count() > 0


class BBTestCase(TestCase):
    login = None

    def setUp(self):
        User.objects.create(
            username='admin_test',
            password='sha1$1073f$68193214ce14f78051d30cbe15691f786761198e',
            is_superuser=True,
            is_active=True,
            is_staff=True,
        )
        if self.login == 'superuser':
            self._login_superuser()

    def _login_superuser(self):
        self.client.login(username='admin_test', password='admin_test')
