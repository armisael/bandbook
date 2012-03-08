"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from operator import attrgetter
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from django.test import TestCase
from bandbook.instruments.models import InstrumentCategory, InstrumentType


class OrderingTest(TestCase):
    fixtures = ['instruments']

    def setUp(self):
        User.objects.create(
            username='admin_test',
            password='sha1$1073f$68193214ce14f78051d30cbe15691f786761198e',
            is_superuser=True,
            is_active=True,
            is_staff=True,
        )
        self.client.login(username='admin_test', password='admin_test')

    @staticmethod
    def _group(sqs, fun):
        d = {}
        for x in sqs:
            k = fun(x)
            if k not in d:
                d[k] = []
            d[k].append(x)
        return d

    def _test_ordering(self, url, model):
        orig_list = model.objects.all()
        ordering_keys = dict([(x.pk, i) for i, x in enumerate(orig_list)])
        orig_positions = range(len(orig_list))
        orig_ordering = [x.ordering for x in orig_list]

        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)

        new_list = [x for x in model.objects.all()]
        new_ordering_keys = dict([(x.pk, i) for i, x in enumerate(new_list)])
        new_positions = [new_ordering_keys[x.pk] for x in orig_list]
        resorted_list = sorted(new_list, key=lambda x: ordering_keys[x.pk])
        new_ordering = [x.ordering for x in resorted_list]

        return orig_positions, orig_ordering, new_positions, new_ordering

    def _test_ordering_with_parent(self, url, model, parent_field):
        orig_list = self._group(model.objects.all(), attrgetter(parent_field))
        ordering_keys = dict((k, dict([(y.pk, i) for i, y in enumerate(orig_list[k])])) for k in orig_list)
        orig_positions = dict((k, range(len(orig_list[k]))) for k in orig_list)
        orig_ordering = dict((k, [x.ordering for x in orig_list[k]]) for k in orig_list)

        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)

        new_list = self._group(model.objects.all(), attrgetter(parent_field))
        new_ordering_keys = dict((k, dict([(y.pk, i) for i, y in enumerate(new_list[k])])) for k in new_list)
        new_positions = dict((k, [new_ordering_keys[k][x.pk] for x in orig_list[k]]) for k in orig_list)
        resorted_list = dict((k, sorted(new_list[k], key=lambda x: ordering_keys[k][x.pk])) for k in new_list)
        new_ordering = dict((k, [x.ordering for x in resorted_list[k]]) for k in resorted_list)

        return orig_positions, orig_ordering, new_positions, new_ordering


    def test_category_ordering_down(self):
        categories = [x for x in InstrumentCategory.objects.all()]
        obja = categories[0]
        objb = categories[2]  # move cat[0] right before cat[2]

        url = reverse('instrumentcategory_order', args=(obja.pk, objb.pk))
        orig_positions, orig_ordering, new_positions, new_ordering = \
            self._test_ordering(url, InstrumentCategory)

        self.assertEqual(orig_positions, [0, 1, 2])
        self.assertEqual(new_positions, [1, 0, 2])
        self.assertEqual(orig_ordering, [1, 2, 3])
        self.assertEqual(new_ordering, [2, 1, 3])


    def test_category_ordering_down_last(self):
        categories = [x for x in InstrumentCategory.objects.all()]
        obja = categories[0]  # move cat[0] to the end

        url = reverse('instrumentcategory_order', args=(obja.pk, -1))
        orig_positions, orig_ordering, new_positions, new_ordering = \
            self._test_ordering(url, InstrumentCategory)

        self.assertEqual(orig_positions, [0, 1, 2])
        self.assertEqual(new_positions, [2, 0, 1])
        self.assertEqual(orig_ordering, [1, 2, 3])
        self.assertEqual(new_ordering, [3, 1, 2])

    def test_category_ordering_up(self):
        categories = [x for x in InstrumentCategory.objects.all()]
        obja = categories[2]
        objb = categories[0]  # move cat[2] right before cat[0]

        url = reverse('instrumentcategory_order', args=(obja.pk, objb.pk))
        orig_positions, orig_ordering, new_positions, new_ordering = \
            self._test_ordering(url, InstrumentCategory)

        self.assertEqual(orig_positions, [0, 1, 2])
        self.assertEqual(new_positions, [1, 2, 0])
        self.assertEqual(orig_ordering, [1, 2, 3])
        self.assertEqual(new_ordering, [2, 3, 1])

    def test_type_ordering_down(self):
        categories = [x for x in InstrumentCategory.objects.all()]
        types = self._group(InstrumentType.objects.all(), lambda x: x.category_id)

        obja = types[categories[0].pk][1]
        objb = types[categories[0].pk][6]

        url = reverse('instrumenttype_order',
                      args=(categories[0].slug, obja.pk, objb.pk))
        orig_positions, orig_ordering, new_positions, new_ordering = \
            self._test_ordering_with_parent(url, InstrumentType,
                                            parent_field='category_id')

        self.assertEqual(orig_positions[categories[0].pk], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.assertEqual(new_positions[categories[0].pk], [0, 5, 1, 2, 3, 4, 6, 7, 8, 9, 10])
        self.assertEqual(orig_positions[categories[1].pk], [0, 1, 2, 3, 4, 5])
        self.assertEqual(new_positions[categories[1].pk], orig_positions[categories[1].pk])
        self.assertEqual(orig_positions[categories[2].pk], [0, 1, 2, 3])
        self.assertEqual(new_positions[categories[2].pk], orig_positions[categories[2].pk])

        self.assertEqual(orig_ordering[categories[0].pk], [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110])
        self.assertEqual(new_ordering[categories[0].pk], [10, 69, 29, 39, 49, 59, 70, 80, 90, 100, 110])
        self.assertEqual(orig_ordering[categories[1].pk], [10, 20, 30, 40, 50, 60])
        self.assertEqual(new_ordering[categories[1].pk], orig_ordering[categories[1].pk])
        self.assertEqual(orig_ordering[categories[2].pk], [10, 20, 30, 40])
        self.assertEqual(new_ordering[categories[2].pk], orig_ordering[categories[2].pk])

    def test_type_ordering_up(self):
        categories = [x for x in InstrumentCategory.objects.all()]
        types = self._group(InstrumentType.objects.all(), lambda x: x.category_id)

        obja = types[categories[0].pk][8]
        objb = types[categories[0].pk][3]

        url = reverse('instrumenttype_order',
                      args=(categories[0].slug, obja.pk, objb.pk))
        orig_positions, orig_ordering, new_positions, new_ordering = \
            self._test_ordering_with_parent(url, InstrumentType,
                                            parent_field='category_id')

        self.assertEqual(orig_positions[categories[0].pk], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.assertEqual(new_positions[categories[0].pk], [0, 1, 2, 4, 5, 6, 7, 8, 3, 9, 10])
        self.assertEqual(orig_positions[categories[1].pk], [0, 1, 2, 3, 4, 5])
        self.assertEqual(new_positions[categories[1].pk], orig_positions[categories[1].pk])
        self.assertEqual(orig_positions[categories[2].pk], [0, 1, 2, 3])
        self.assertEqual(new_positions[categories[2].pk], orig_positions[categories[2].pk])

        self.assertEqual(orig_ordering[categories[0].pk], [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110])
        self.assertEqual(new_ordering[categories[0].pk], [10, 20, 30, 41, 51, 61, 71, 81, 40, 100, 110])
        self.assertEqual(orig_ordering[categories[1].pk], [10, 20, 30, 40, 50, 60])
        self.assertEqual(new_ordering[categories[1].pk], orig_ordering[categories[1].pk])
        self.assertEqual(orig_ordering[categories[2].pk], [10, 20, 30, 40])
        self.assertEqual(new_ordering[categories[2].pk], orig_ordering[categories[2].pk])

    def test_type_ordering_down_last(self):
        categories = [x for x in InstrumentCategory.objects.all()]
        types = self._group(InstrumentType.objects.all(), lambda x: x.category_id)

        obja = types[categories[0].pk][4]

        url = reverse('instrumenttype_order',
                      args=(categories[0].slug, obja.pk, -1))
        orig_positions, orig_ordering, new_positions, new_ordering = \
            self._test_ordering_with_parent(url, InstrumentType,
                                            parent_field='category_id')

        self.assertEqual(orig_positions[categories[0].pk], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.assertEqual(new_positions[categories[0].pk], [0, 1, 2, 3, 10, 4, 5, 6, 7, 8, 9])
        self.assertEqual(orig_positions[categories[1].pk], [0, 1, 2, 3, 4, 5])
        self.assertEqual(new_positions[categories[1].pk], orig_positions[categories[1].pk])
        self.assertEqual(orig_positions[categories[2].pk], [0, 1, 2, 3])
        self.assertEqual(new_positions[categories[2].pk], orig_positions[categories[2].pk])

        self.assertEqual(orig_ordering[categories[0].pk], [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110])
        self.assertEqual(new_ordering[categories[0].pk], [10, 20, 30, 40, 110, 59, 69, 79, 89, 99, 109])
        self.assertEqual(orig_ordering[categories[1].pk], [10, 20, 30, 40, 50, 60])
        self.assertEqual(new_ordering[categories[1].pk], orig_ordering[categories[1].pk])
        self.assertEqual(orig_ordering[categories[2].pk], [10, 20, 30, 40])
        self.assertEqual(new_ordering[categories[2].pk], orig_ordering[categories[2].pk])



class InstrumentTypeViews(TestCase):
    def test_change_category(self):
        type = InstrumentType.objects.all()[18]
        category = InstrumentCategory.objects.filter(pk__not=type.category_id)[0]

        url = reverse('instrumenttype_update', args=(type.category.slug, type.pk))
        response = self.client.post(url, {
            'name':
        })
