from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ObjectDoesNotExist, EmptyResultSet, ValidationError
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.urls import reverse
from .models import Company, Commercial, Manager, Client, Service, License
from .forms import ServiceForm, ClientForm
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
        return routeCreatePermissions(self, self.kwargs.get(self.pk_url_kwarg))

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
    extra_context = {"update": True, "button": "Confirmer"}

    def test_func(self):
        return routeUpdatePermissions(self, self.pk_url_kwarg, Client)

    def get_success_url(self):
        return self.object.get_absolute_url(self.object.company.id)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ClientUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Client
    template_name = 'mvp/clients/client_details.html'
    object = None
    pk_url_kwarg = 'client_pk'
    extra_context = {"delete": True, "button": "Delete"}

    def test_func(self):
        return routeDeletePermissions(self, self.pk_url_kwarg, Client)

    def get_success_url(self):
        if hasattr(self.request.user, 'commercial'):
            return reverse('mvp-client-list', args=[self.object.company.id, self.request.user.commercial.id])
        elif hasattr(self.request.user, 'manager'):
            return reverse('mvp-client-list', args=[self.object.company.id, self.request.user.manager.id])
        else:
            return redirect('mvp-workspace')


    # def get_form_kwargs(self, *args, **kwargs):
    #     kwargs = super(ClientDeleteView, self).get_form_kwargs()
    #     kwargs['user'] = self.request.user
    #     return kwargs


class ClientListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Client
    template_name = 'mvp/clients/client_list.html'
    ordering = ['id']
    pk_url_kwarg = 'com_pk'

    def get_queryset(self):
        if hasattr(self.request.user, 'commercial'):
            client = Client.objects.filter(commercial=self.request.user.commercial)
            if client.exists():
                return client
        try:
            client = Client.objects.filter(company=self.request.user.manager.company)
            if client.exists():
                return client
        except ObjectDoesNotExist:
            return HttpResponseForbidden
        else:
            return HttpResponseNotFound

    def test_func(self):
        # @TODO Faire try except Permission denied ?
        return routeListPermissions(self, self.pk_url_kwarg)


class ClientDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Client
    template_name = 'mvp/clients/client_details.html'
    pk_url_kwarg = 'client_pk'
    extra_context = {"button": "Modifier"}

    def get_queryset(self):
        return Client.objects.filter(id=self.kwargs.get(self.pk_url_kwarg))

    def test_func(self):
        # @TODO Faire try except Permission denied ?
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


class ServiceDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
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
        return routeListPermissions(self, self.pk_url_kwarg)


class LicenseDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
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
