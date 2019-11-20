from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ObjectDoesNotExist, EmptyResultSet, ValidationError
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.urls import reverse
from .models import Company, Commercial, Manager, Client, Service, License
from .forms import ClientForm, ServiceForm, LicenseForm
from .controllers import (
    routeListPermissions,
    routeDetailsPermissions,
    routeCreatePermissions,
    routeUpdatePermissions,
    routeDeletePermissions,
    validateCompanyInFormCreateUpdateView,
)


class ClientCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'mvp/clients/client_form.html'
    object = None
    pk_url_kwarg = 'cpny_pk'
    extra_context = {"button": "Ajouter un client"}

    def form_valid(self, form):
        return validateCompanyInFormCreateUpdateView(self, form)

    def test_func(self):
        return routeCreatePermissions(self, self.kwargs.get(self.pk_url_kwarg), self.model)

    def get_success_url(self):
        return self.object.get_absolute_url(self.object.company.id)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ClientCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Client
    form_class = ClientForm
    object = None
    template_name = 'mvp/clients/client_form.html'
    pk_url_kwarg = 'client_pk'
    extra_context = {"update": True, "button": "Update"}

    def test_func(self):
        return routeUpdatePermissions(self, self.pk_url_kwarg, self.model)

    def get_success_url(self):
        return self.object.get_absolute_url(self.object.company.id)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ClientUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ClientListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Client
    template_name = 'mvp/clients/client_list.html'
    ordering = ['id']
    pk_url_kwarg = 'com_pk'

    def get_queryset(self):
        if hasattr(self.request.user, 'commercial'):
            # @TODO: a remplacer  pour Service et client ??
            return self.request.user.commercial.client_set.all()
            # client = Client.objects.filter(commercial=self.request.user.commercial)
            # if client.exists():
            #     return client
        try:
            # @TODO: a remplacer  pour Service et client ??
            return self.request.user.manager.company.client_set.all()
            # client = Client.objects.filter(company=self.request.user.manager.company)
            # if client.exists():
            #     return client
        except ObjectDoesNotExist:
            return HttpResponseNotFound
            # return HttpResponseForbidden
        # else:
        #     return HttpResponseNotFound

    def test_func(self):
        # @TODO Faire try except Permission denied ?
        return routeListPermissions(self, self.pk_url_kwarg)


class ClientDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Client
    template_name = 'mvp/clients/client_details.html'
    pk_url_kwarg = 'client_pk'
    extra_context = {"button_update": "Update", "button_delete": "Delete"}

    def get_queryset(self):
        # @TODO: Faire try except empty querryset ?
        return Client.objects.filter(id=self.kwargs.get(self.pk_url_kwarg))

    def test_func(self):
        # @TODO Faire try except Permission denied ?
        return routeDetailsPermissions(self, self.pk_url_kwarg, self.model)


class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Client
    template_name = 'mvp/clients/client_details.html'
    object = None
    pk_url_kwarg = 'client_pk'
    extra_context = {"delete": True, "button": "Delete"}

    def test_func(self):
        return routeDeletePermissions(self, self.pk_url_kwarg, self.model)

    def get_success_url(self):
        if hasattr(self.request.user, 'commercial'):
            return reverse('mvp-client-list', args=[self.object.company.id, self.request.user.commercial.id])
        elif hasattr(self.request.user, 'manager'):
            return reverse('mvp-client-list', args=[self.object.company.id, self.request.user.manager.id])
        else:
            return redirect('mvp-workspace')


class ServiceCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'mvp/service/service_form.html'
    object = None
    pk_url_kwarg = 'cpny_pk'
    extra_context = {"button": "Ajouter un Service"}

    def form_valid(self, form):
        return validateCompanyInFormCreateUpdateView(self, form)

    def test_func(self):
        return routeCreatePermissions(self, self.kwargs.get(self.pk_url_kwarg), self.model)

    def get_success_url(self):
        return self.object.get_absolute_url(self.object.company.id)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ServiceCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ServiceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Service
    form_class = ServiceForm
    object = None
    template_name = 'mvp/service/service_form.html'
    pk_url_kwarg = 'service_pk'
    extra_context = {"update": True, "button": "Update"}

    def test_func(self):
        return routeUpdatePermissions(self, self.pk_url_kwarg, self.model)

    def get_success_url(self):
        return self.object.get_absolute_url(self.object.company.id)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ServiceUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ServiceListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Service
    template_name = 'mvp/service/service_list.html'
    ordering = ['id']
    pk_url_kwarg = 'com_pk'

    def get_queryset(self):
        if hasattr(self.request.user, 'commercial'):
            # @TODO: a remplacer  pour Service et client ??
            return self.request.user.commercial.service_set.all()
            # service = Service.objects.filter(commercial=self.request.user.commercial)
            # if service.exists():
            #     return service
        try:
            # @TODO: a remplacer  pour Service et client ??
            return self.request.user.manager.company.service_set.all()
            # service = Service.objects.filter(company=self.request.user.manager.company)
            # if service.exists():
            #     return service
        except ObjectDoesNotExist:
            return HttpResponseNotFound
            # return HttpResponseForbidden
        # else:
        #     return HttpResponseNotFound

    def test_func(self):
        return routeListPermissions(self, self.pk_url_kwarg)


class ServiceDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Service
    template_name = 'mvp/service/service_details.html'
    pk_url_kwarg = 'service_pk'
    extra_context = {"button_update": "Update", "button_delete": "Delete"}

    def get_queryset(self):
        # @TODO: Faire try except empty querryset ?
        return Service.objects.filter(id=self.kwargs.get(self.pk_url_kwarg))

    def test_func(self):
        # @TODO Faire try except Permission denied ?
        return routeDetailsPermissions(self, self.pk_url_kwarg, self.model)


class ServiceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Service
    template_name = 'mvp/service/service_details.html'
    object = None
    pk_url_kwarg = 'service_pk'
    extra_context = {"delete": True, "button": "Delete"}

    def test_func(self):
        return routeDeletePermissions(self, self.pk_url_kwarg, self.model)

    def get_success_url(self):
        if hasattr(self.request.user, 'commercial'):
            return reverse('mvp-service-list', args=[self.object.company.id, self.request.user.commercial.id])
        elif hasattr(self.request.user, 'manager'):
            return reverse('mvp-service-list', args=[self.object.company.id, self.request.user.manager.id])
        else:
            return redirect('mvp-workspace')


class LicenseCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = License
    form_class = LicenseForm
    template_name = 'mvp/license/license_form.html'
    object = None
    pk_url_kwarg = 'cpny_pk'
    extra_context = {"button": "Ajouter une License"}

    def form_valid(self, form):
        return validateCompanyInFormCreateUpdateView(self, form)

    def test_func(self):
        return routeCreatePermissions(self, self.kwargs.get(self.pk_url_kwarg), self.model)

    def get_success_url(self):
        return self.object.get_absolute_url(self.object.company.id)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(LicenseCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class LicenseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = License
    form_class = LicenseForm
    object = None
    template_name = 'mvp/license/license_form.html'
    pk_url_kwarg = 'license_pk'
    extra_context = {"update": True, "button": "Update"}

    def test_func(self):
        return routeUpdatePermissions(self, self.pk_url_kwarg, self.model)

    def get_success_url(self):
        return self.object.get_absolute_url(self.object.company.id)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(LicenseUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class LicenseListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = License
    template_name = 'mvp/license/license_list.html'
    pk_url_kwarg = 'com_pk'
    ordering = ['id']

    def get_queryset(self):
        if hasattr(self.request.user, 'commercial'):
            # @TODO: a remplacer  pour Service et client ??
            return self.request.user.commercial.license_set.all()
            # licenses_found = License.objects.filter(commercial=self.request.user.commercial)
            # if licenses_found.exists():
            #     return licenses_found
        try:
            # @TODO: a remplacer  pour Service et client ??
            return self.request.user.manager.company.license_set.all()
            # licenses_found = License.objects.filter(company=self.request.user.manager.company)
            # if licenses_found.exists():
            #     return licenses_found
        except ObjectDoesNotExist:
            return HttpResponseNotFound
            # return HttpResponseForbidden
        # else:
        #     return HttpResponseNotFound

    def test_func(self):
        return routeListPermissions(self, self.pk_url_kwarg)


class LicenseDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = License
    template_name = 'mvp/license/license_details.html'
    pk_url_kwarg = 'license_pk'
    extra_context = {"button_update": "Update", "button_delete": "Delete"}

    def get_queryset(self):
        # @TODO: Faire try except empty querryset ?
        return License.objects.filter(pk=self.kwargs.get(self.pk_url_kwarg))

    def test_func(self):
        # @TODO Faire try except Permission denied ?
        return routeDetailsPermissions(self, self.pk_url_kwarg, self.model)


class LicenseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = License
    template_name = 'mvp/license/license_details.html'
    object = None
    pk_url_kwarg = 'license_pk'
    extra_context = {"delete": True, "button": "Delete"}

    def test_func(self):
        return routeDeletePermissions(self, self.pk_url_kwarg, self.model)

    def get_success_url(self):
        if hasattr(self.request.user, 'commercial'):
            return reverse('mvp-license-list', args=[self.object.company.id, self.request.user.commercial.id])
        elif hasattr(self.request.user, 'manager'):
            return reverse('mvp-license-list', args=[self.object.company.id, self.request.user.manager.id])
        else:
            return redirect('mvp-workspace')


