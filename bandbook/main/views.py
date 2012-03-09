import cgi
import logging
import cStringIO as StringIO
from datetime import datetime
from django.conf.urls.defaults import url
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models.expressions import F
from django.template.loader import get_template
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template.context import RequestContext, Context
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from xhtml2pdf import pisa
from bandbook.instruments.helpers import get_default_ordering
from bandbook.main.helpers import index_block, reverse_lazy, filter_queryset

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def about(request):
    return render_to_response('about.html', None,
                              context_instance=RequestContext(request))


def login_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    referer = request.META.get('HTTP_REFERER')

    if user is not None:
        if user.is_active:
            login(request, user)
        else:
            messages.error(request,
                       _('This account has been disabled. Sorry for that!'))
    else:
        messages.error(request,
                       _('Wrong username or password'))

    if referer:
        return HttpResponseRedirect(referer)
    HttpResponseRedirect('/')


def logout_view(request):
    logout(request)
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return HttpResponseRedirect(referer)
    return HttpResponseRedirect(reverse('index'))


def close_modal(request):
    return render_to_response('close_modal.html', {
        'reload': True,
    }, context_instance=RequestContext(request))


def index(request):
    blocks = [
        index_block(100, 70, 100, 'se', url='scores/', img_class='scores'),
        index_block(100, 70, 50, 'sw', style='warning'),
        index_block(100, 70, 74, 'nw', style='info'),
        index_block(100, 70, 35, 'ne', style='success'),

        index_block(312, 283, 45, 'ne', style='warning'),
        index_block(312, 283, 35, 'se', style='info'),
        index_block(312, 283, 20, 'sw', style='success'),

        index_block(312, 322, 24, 'sw', style='error'),
        index_block(312, 322, 10, 'se', style='warning'),
        index_block(147, 350, 100, 'se', url='players/', img_class='players'),

        index_block(285, 488, 25, 'se', style='warning'),
        index_block(285, 488, 45, 'ne', style='error'),
        index_block(334, 488, 20, 'se', style='info'),
        index_block(334, 488, 75, 'ne', style='success'),

        index_block(413, 409, 35, 'nw', style='error'),
        index_block(413, 410, 10, 'ne', style='warning'),
        index_block(413, 410, 30, 'se', style='info'),
        index_block(427, 233, 100, 'se', url='instruments/',
                    img_class='instruments'),

        index_block(589, 395, 40, 'ne', style='info'),
        index_block(589, 395, 30, 'se', style='warning'),
        index_block(589, 395, 20, 'sw', style='error'),

        index_block(312, 70, 20, 'ne', style='info'),
        index_block(336, 70, 15, 'sw', style='error'),

        index_block(385, 70, 100, 'se', style='info'),
        index_block(385, 70, 35, 'sw', style='warning'),
        index_block(385, 70, 25, 'ne', style='error'),
        index_block(385, 70, 45, 'nw', style='success'),

        index_block(489, 174, 30, 'sw', style='success'),
        index_block(489, 174, 20, 'ne', style='warning'),
        index_block(489, 174, 40, 'se', style='error'),

        index_block(385, 174, 15, 'sw', style='error'),
        index_block(385, 227, 30, 'ne', style='success'),
        index_block(371, 227, 10, 'se', style='warning'),
        index_block(371, 227, 6, 'sw', style='info'),

        index_block(419, 227, 5, 'se', style='warning'),

        index_block(580, 187, 20, 'sw', style='warning'),
        index_block(580, 211, 5, 'se', style='info'),
        index_block(589, 220, 10, 'se', style='error'),
        index_block(580, 0, 185, 'se', url='events/', tmpl_class='events'),

    ]
    return render_to_response('index.html', {
        'blocks': blocks,
    }, context_instance=RequestContext(request))


class PrintView(DetailView):
    template_name_suffix = '_pdf'

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(PrintView, self).dispatch(*args, **kwargs)

    def get(self, request, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        if 'filename' not in context:
            context['filename'] = self.object._meta.object_name.lower()
            attr = 'slug' if hasattr(self.object, 'slug') else 'pk'
            context['filename'] += "_%s" % getattr(self.object, attr)

        template = self.get_template_names()[0]
        return render_to_pdf(template, context)


# TODO che succede se sposto un elemento in un'altra lista? Broken!
# TODO v problemi spostando in ultima posizione se ci sono buchi..
# TODO v ordinamento non e' parent-aware!
class OrderView(View):
    model = None

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(OrderView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        pka = kwargs.get('pka')
        pkb = kwargs.get('pkb')
        parent_field = None

        if pka is None or pkb is None:
            return HttpResponse(status=400)

        try:
            obja = self.model._default_manager.get(pk=pka)
            objb = self.model._default_manager.get(pk=pkb) \
                    if pkb != "-1" else None
        except self.model.DoesNotExist:
            raise Http404

        moving_down = objb is None or obja.ordering < objb.ordering
        conditions = ['gt', 'lt'] if moving_down else ['lt', 'gte']
        offset = -1 if moving_down else 1
        filters = {
            'ordering__%s' % conditions.pop(0): obja.ordering
        }
        if objb is not None:
            filters['ordering__%s' % conditions.pop(0)] = objb.ordering
        if hasattr(obja, 'parent_model'):
            parent_field = '%s' % obja.parent_model[0]
            filters[parent_field] = getattr(obja, parent_field)

        self.model._default_manager.filter(**filters)\
                    .update(ordering=F('ordering') + offset)

        target_ordering = objb.ordering - 1 if objb is not None \
                                            else get_default_ordering(
                                                    self.model,
                                                    filters.get(parent_field))
        if not moving_down:
            target_ordering += 1
        self.model._default_manager.filter(pk=obja.pk)\
                                    .update(ordering=target_ordering)

        return HttpResponse(status=200)


class _BBListView(ListView):
    def get_queryset(self):
        sqs = super(_BBListView, self).get_queryset()

        query = self.request.GET.get('q')
        if query and hasattr(self.model, 'search_by'):
            sqs = filter_queryset(sqs, query, getattr(self.model, 'search_by'))

        return sqs


class _BBCreateView(CreateView):
    success_url = reverse_lazy('close_modal')
    parent = None

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(_BBCreateView, self).dispatch(*args, **kwargs)

    def get_initial(self):
        initials = {}
        if self.parent is not None:
            param = self.kwargs.get(self.parent['param'])
            obj = self.parent['model']._default_manager.get(
                **{self.parent['param']: param})
            initials.update({
                self.parent['field']: obj,
            })
        return initials


class _BBUpdateView(UpdateView):

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(_BBUpdateView, self).dispatch(*args, **kwargs)


class _BBDeleteView(DeleteView):

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(_BBDeleteView, self).dispatch(*args, **kwargs)


class BBView(object):
    model = None
    form_class = None
    parent = None

    @classmethod
    def as_list_view(cls):
        return _BBListView.as_view(model=cls.model)

    @classmethod
    def as_detail_view(cls):
        return DetailView.as_view(model=cls.model)

    @classmethod
    def as_create_view(cls):
        return _BBCreateView.as_view(model=cls.model,
                                     form_class=cls.form_class,
                                     parent=cls.parent)

    @classmethod
    def as_update_view(cls):
        return _BBUpdateView.as_view(model=cls.model,
                                     form_class=cls.form_class,
                                     success_url=reverse_lazy('close_modal'))

    @classmethod
    def as_delete_view(cls):
        return _BBDeleteView.as_view(model=cls.model,
                                     success_url=reverse_lazy('close_modal'),
                                     template_name='layouts/delete_base.html')

    @classmethod
    def as_order_view(cls):
        return OrderView.as_view(model=cls.model)

    @classmethod
    def as_print_view(cls):
        return PrintView.as_view(model=cls.model)

    @classmethod
    def urls(cls, prefix, actions, uregex='(?P<pk>\d+)'):
        _urls = []
        for action in actions:
            path = '^%s/' % prefix if prefix else '^'
            if action in ['detail', 'update', 'delete', 'print']:
                path += '%s/' % uregex
            if action == 'order':
                path += '(?P<pka>\d+)/(?P<pkb>-?\d+)/'
            if action not in ['list', 'detail']:
                path += '%s/' % action
            path += '$'
            name = '%s_%s' % (cls.model._meta.object_name.lower(), action)
            view = getattr(cls, 'as_%s_view' % action)()

            _urls.append(url(path, view, name=name))
        return _urls


def render_to_pdf(template_src, context_dict):
    # doc: http://xhtml2pdf.appspot.com/static/pisa-en.html
    # see http://tinyurl.com/87ncxd3 for header/footer configuration
    template = get_template(template_src)
    context = Context(context_dict)
    html = template.render(context)
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(
        StringIO.StringIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        if 'filename' not in context_dict:
            context_dict['filename'] = ''.join(
                [str(x) for x in datetime.utcnow().timetuple() if x >= 0])
        filename = '%s.pdf' % context_dict['filename']
        response = HttpResponse(result.getvalue(),
                                mimetype='application/pdf',
                                content_type='application/pdf')
        response['Content-Disposition'] = 'filename=%s' % filename
        return response
    return HttpResponse('PDF generation error: <pre>%s</pre>' %
                        cgi.escape(html), status=500)
