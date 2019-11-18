from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ObjectDoesNotExist, EmptyResultSet
from django.shortcuts import redirect, get_object_or_404
from django.http import Http404
from .models import Company, Commercial, Manager, Client, Service, License
from .forms import ServiceForm, ClientForm
from .controllers import routeListPermissions, routeDetailsPermissions


class ClientListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Client
    template_name = 'mvp/clients/client_list.html'
    ordering = ['id']
    pk_url_kwarg = 'com_pk'

    def get_queryset(self):
        try:
            return Client.objects.filter(commercial=self.request.user.commercial)
        except ObjectDoesNotExist:
            return Client.objects.filter(company=self.request.user.manager.company)
        # finally: (pas ça)
        #     return Http404
        # @TODO: RAISE ERROR 404

    def test_func(self):
        return routeListPermissions(self, self.pk_url_kwarg)


class ClientDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Client
    template_name = 'mvp/clients/client_details.html'
    pk_url_kwarg = 'client_pk'

    def get_queryset(self):
        return Client.objects.filter(id=self.kwargs.get(self.pk_url_kwarg))

    def test_func(self):
        return routeDetailsPermissions(self, self.pk_url_kwarg, self.model)


class ServiceListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Service
    template_name = 'mvp/service/service_list.html'
    ordering = ['id']
    pk_url_kwarg = 'com_pk'

    def get_queryset(self):
        try:
            return Service.objects.filter(commercial=self.request.user.commercial)
        except ObjectDoesNotExist:
            return Service.objects.filter(company=self.request.user.manager.company)
        # @TODO: RAISE ERROR 404

    def test_func(self):
        return routeListPermissions(self, self.pk_url_kwarg)


class ServiceDetailView(DetailView):
    model = Service
    template_name = 'mvp/service/service_details.html'
    pk_url_kwarg = 'service_pk'

    def get_queryset(self):
        return Service.objects.filter(id=self.kwargs.get(self.pk_url_kwarg))

    def test_func(self):
        return routeDetailsPermissions(self, self.pk_url_kwarg, self.model)


class LicenseListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = License
    template_name = 'mvp/license/license_list.html'
    pk_url_kwarg = 'com_pk'
    ordering = ['id']

    def get_queryset(self):
        try:
            return License.objects.filter(commercial=self.request.user.commercial)
        except ObjectDoesNotExist:
            return License.objects.filter(company=self.request.user.manager.company)
        # @TODO: RAISE ERROR 404

    def test_func(self):
        return routeDetailsPermissions(self, self.pk_url_kwarg, self.model)


class LicenseDetailView(DetailView):
    model = License
    template_name = 'mvp/license/license_details.html'
    pk_url_kwarg = 'license_pk'

    def get_queryset(self):
        return License.objects.filter(pk=self.kwargs.get(self.pk_url_kwarg))

    def test_func(self):
        return routeDetailsPermissions(self, self.pk_url_kwarg, self.model)


# @TODO: A modifier
class ServiceUpdateView(UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'mvp/forms/service_form.html'

    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(request.POST, request.user)
    #     form.save()

    def get_queryset(self):
        return Service.objects.filter(pk=self.kwargs.get('pk'))


# @login required
# class ClientCreateView(LoginRequiredMixin, UserPassesTestMixin,CreateView):
class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'mvp/forms/client_form.html'
    # @TODO peut etre a remove
    object = None

    def form_valid(self, form):
        self.object = form.save(commit=False, user=self.request.user)
        if hasattr(self.request.user, 'commercial'):
            self.object.company = self.request.user.commercial.company
        else:
            self.object.company = self.request.user.manager.company
        self.object.save()
        return redirect(self.get_success_url())

    def test_func(self):


    # def get(self, request, *args, **kwargs):
    #     print('ee')
    #     self.user = request.user
    #     return super(ClientCreateView, self).get(request, *args, **kwargs)
    #
    # def post(self, request, *args, **kwargs):
    #     print('post')
    #     return super(ClientCreateView, self).post(request, *args, user=request.user, **kwargs)
    #
    # def form_invalid(self, form):
    #     print('invalid')
    #     return super(ClientCreateView, self).form_invalid(form)

    def get_success_url(self):
        return self.object.get_absolute_url(self.object.company.id)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ClientCreateView, self).get_form_kwargs(*args, **kwargs)
        # kwargs = super(ClientCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
