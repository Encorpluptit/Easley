from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ObjectDoesNotExist, EmptyResultSet, ValidationError
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.urls import reverse
from .models import Company, Commercial, Manager, Client, Service, License, Invoice
from .forms import ClientForm, ServiceForm, LicenseForm, InvoiceFrom
from .controllers import (
    routeListPermissions,
    routeDetailsPermissions,
    routeCreatePermissions,
    routeUpdatePermissions,
    routeDeletePermissions,
    validateCompanyInFormCreateUpdateView,
    routeCreateUpdateInvoicePermissions,
    routeListDetailsInvoicePermissions,
    redirectWorkspaceFail,
)


class ClientCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'mvp/client/client_form.html'
    object = None
    pk_url_kwarg = 'cpny_pk'
    extra_context = {"button": "Ajouter un client"}
    permission_denied_message = f"Vous n'avez pas la permission de voir cette page."

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

    def handle_no_permission(self):
        return redirectWorkspaceFail(self.request, self.permission_denied_message)


class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'mvp/client/client_form.html'
    object = None
    pk_url_kwarg = 'client_pk'
    extra_context = {"update": True, "button": "Update"}
    permission_denied_message = f"Vous n'avez pas la permission de voir cette page."

    def test_func(self):
        return routeUpdatePermissions(self, self.pk_url_kwarg, self.model)

    def get_success_url(self):
        return self.object.get_absolute_url(self.object.company.id)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ClientUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def handle_no_permission(self):
        return redirectWorkspaceFail(self.request, self.permission_denied_message)


class ClientListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Client
    template_name = 'mvp/client/client_list.html'
    ordering = ['id']
    pk_url_kwarg = 'com_pk'
    permission_denied_message = f"Vous n'avez pas la permission de voir cette page."

    def get_queryset(self):
        if hasattr(self.request.user, 'commercial'):
            return self.request.user.commercial.client_set.all()
        elif hasattr(self.request.user, 'manager'):
            return self.request.user.manager.company.client_set.all()
        else:
            return HttpResponseNotFound

    def test_func(self):
        return routeListPermissions(self, self.pk_url_kwarg)

    def handle_no_permission(self):
        return redirectWorkspaceFail(self.request, self.permission_denied_message)


class ClientDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Client
    template_name = 'mvp/client/client_details.html'
    pk_url_kwarg = 'client_pk'
    extra_context = {"button_update": "Update", "button_delete": "Delete"}
    permission_denied_message = f"Vous n'avez pas la permission de voir cette page."

    def get_queryset(self):
        # @TODO: Faire try except empty querryset ?
        return Client.objects.filter(id=self.kwargs.get(self.pk_url_kwarg))

    def test_func(self):
        return routeDetailsPermissions(self, self.pk_url_kwarg, self.model)

    def handle_no_permission(self):
        return redirectWorkspaceFail(self.request, self.permission_denied_message)


class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Client
    template_name = 'mvp/client/client_details.html'
    object = None
    pk_url_kwarg = 'client_pk'
    extra_context = {"delete": True, "button": "Delete"}
    permission_denied_message = f"Vous n'avez pas la permission de voir cette page."

    def test_func(self):
        return routeDeletePermissions(self, self.pk_url_kwarg, self.model)

    def get_success_url(self):
        if hasattr(self.request.user, 'commercial'):
            return reverse('mvp-client-list', args=[self.object.company.id, self.request.user.commercial.id])
        elif hasattr(self.request.user, 'manager'):
            return reverse('mvp-client-list', args=[self.object.company.id, self.request.user.manager.id])
        else:
            return redirect('mvp-workspace')

    def handle_no_permission(self):
        return redirectWorkspaceFail(self.request, self.permission_denied_message)


class ServiceCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'mvp/service/service_form.html'
    object = None
    pk_url_kwarg = 'cpny_pk'
    extra_context = {"button": "Ajouter un Service"}
    permission_denied_message = f"Vous n'avez pas la permission de voir cette page."

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

    def handle_no_permission(self):
        return redirectWorkspaceFail(self.request, self.permission_denied_message)


class ServiceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'mvp/service/service_form.html'
    object = None
    pk_url_kwarg = 'service_pk'
    extra_context = {"update": True, "button": "Update"}
    permission_denied_message = f"Vous n'avez pas la permission de voir cette page."

    def test_func(self):
        return routeUpdatePermissions(self, self.pk_url_kwarg, self.model)

    def get_success_url(self):
        return self.object.get_absolute_url(self.object.company.id)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ServiceUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def handle_no_permission(self):
        return redirectWorkspaceFail(self.request, self.permission_denied_message)


class ServiceListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Service
    template_name = 'mvp/service/service_list.html'
    ordering = ['id']
    pk_url_kwarg = 'com_pk'
    permission_denied_message = f"Vous n'avez pas la permission de voir cette page."

    def get_queryset(self):
        if hasattr(self.request.user, 'commercial'):
            return self.request.user.commercial.service_set.all()
        elif hasattr(self.request.user, 'manager'):
            return self.request.user.manager.company.service_set.all()
        else:
            return HttpResponseNotFound

    def test_func(self):
        return routeListPermissions(self, self.pk_url_kwarg)

    def handle_no_permission(self):
        return redirectWorkspaceFail(self.request, self.permission_denied_message)


class ServiceDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Service
    template_name = 'mvp/service/service_details.html'
    pk_url_kwarg = 'service_pk'
    extra_context = {"button_update": "Update", "button_delete": "Delete"}
    permission_denied_message = f"Vous n'avez pas la permission de voir cette page."

    def get_queryset(self):
        # @TODO: Faire try except empty querryset ?
        return Service.objects.filter(id=self.kwargs.get(self.pk_url_kwarg))

    def test_func(self):
        return routeDetailsPermissions(self, self.pk_url_kwarg, self.model)

    def handle_no_permission(self):
        return redirectWorkspaceFail(self.request, self.permission_denied_message)


class ServiceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Service
    template_name = 'mvp/service/service_details.html'
    object = None
    pk_url_kwarg = 'service_pk'
    extra_context = {"delete": True, "button": "Delete"}
    permission_denied_message = f"Vous n'avez pas la permission de voir cette page."

    def test_func(self):
        return routeDeletePermissions(self, self.pk_url_kwarg, self.model)

    def get_success_url(self):
        if hasattr(self.request.user, 'commercial'):
            return reverse('mvp-service-list', args=[self.object.company.id, self.request.user.commercial.id])
        elif hasattr(self.request.user, 'manager'):
            return reverse('mvp-service-list', args=[self.object.company.id, self.request.user.manager.id])
        else:
            return redirect('mvp-workspace')

    def handle_no_permission(self):
        return redirectWorkspaceFail(self.request, self.permission_denied_message)


class LicenseCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = License
    form_class = LicenseForm
    template_name = 'mvp/license/license_form.html'
    object = None
    pk_url_kwarg = 'cpny_pk'
    extra_context = {"button": "Ajouter une License"}
    permission_denied_message = f"Vous n'avez pas la permission de voir cette page."

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

    def handle_no_permission(self):
        return redirectWorkspaceFail(self.request, self.permission_denied_message)


class LicenseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = License
    form_class = LicenseForm
    template_name = 'mvp/license/license_form.html'
    object = None
    pk_url_kwarg = 'license_pk'
    extra_context = {"update": True, "button": "Update"}
    permission_denied_message = f"Vous n'avez pas la permission de voir cette page."

    def test_func(self):
        return routeUpdatePermissions(self, self.pk_url_kwarg, self.model)

    def get_success_url(self):
        return self.object.get_absolute_url(self.object.company.id)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(LicenseUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def handle_no_permission(self):
        return redirectWorkspaceFail(self.request, self.permission_denied_message)


class LicenseListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = License
    template_name = 'mvp/license/license_list.html'
    pk_url_kwarg = 'com_pk'
    ordering = ['id']
    permission_denied_message = f"Vous n'avez pas la permission de voir cette page."

    def get_queryset(self):
        if hasattr(self.request.user, 'commercial'):
            return self.request.user.commercial.license_set.all()
        elif hasattr(self.request.user, 'manager'):
            return self.request.user.manager.company.license_set.all()
        else:
            return HttpResponseNotFound

    def test_func(self):
        return routeListPermissions(self, self.pk_url_kwarg)

    def handle_no_permission(self):
        return redirectWorkspaceFail(self.request, self.permission_denied_message)


class LicenseDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = License
    template_name = 'mvp/license/license_details.html'
    pk_url_kwarg = 'license_pk'
    extra_context = {"button_update": "Update", "button_delete": "Delete"}
    permission_denied_message = f"Vous n'avez pas la permission de voir cette page."

    def get_queryset(self):
        # @TODO: Faire try except empty querryset ?
        return License.objects.filter(pk=self.kwargs.get(self.pk_url_kwarg))

    def test_func(self):
        return routeDetailsPermissions(self, self.pk_url_kwarg, self.model)

    def handle_no_permission(self):
        return redirectWorkspaceFail(self.request, self.permission_denied_message)


class LicenseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = License
    template_name = 'mvp/license/license_details.html'
    object = None
    pk_url_kwarg = 'license_pk'
    extra_context = {"delete": True, "button": "Delete"}
    permission_denied_message = f"Vous n'avez pas la permission de voir cette page."

    def test_func(self):
        return routeDeletePermissions(self, self.pk_url_kwarg, self.model)

    def get_success_url(self):
        if hasattr(self.request.user, 'commercial'):
            return reverse('mvp-license-list', args=[self.object.company.id, self.request.user.commercial.id])
        elif hasattr(self.request.user, 'manager'):
            return reverse('mvp-license-list', args=[self.object.company.id, self.request.user.manager.id])
        else:
            return redirect('mvp-workspace')

    def handle_no_permission(self):
        return redirectWorkspaceFail(self.request, self.permission_denied_message)


class InvoiceCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Invoice
    form_class = InvoiceFrom
    template_name = 'mvp/invoice/invoice_form.html'
    object = None
    pk_url_kwarg = 'cpny_pk'
    extra_context = {"button": "Ajouter une facture"}
    permission_denied_message = f"Vous n'avez pas la permission de voir cette page."

    def form_valid(self, form):
        return validateCompanyInFormCreateUpdateView(self, form)

    def test_func(self):
        return routeCreateUpdateInvoicePermissions(self, self.kwargs.get(self.pk_url_kwarg))

    def get_success_url(self):
        return self.object.get_absolute_url(self.object.company.id)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(InvoiceCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def handle_no_permission(self):
        return redirectWorkspaceFail(self.request, self.permission_denied_message)


class InvoiceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Invoice
    form_class = InvoiceFrom
    template_name = 'mvp/invoice/invoice_form.html'
    object = None
    pk_url_kwarg = 'invoice_pk'
    extra_context = {"update": True, "button": "Update"}
    permission_denied_message = f"Vous n'avez pas la permission de voir cette page."

    def test_func(self):
        return routeCreateUpdateInvoicePermissions(self, self.kwargs.get('cpny_pk'))

    def get_success_url(self):
        return self.object.get_absolute_url(self.object.company.id)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(InvoiceUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def handle_no_permission(self):
        return redirectWorkspaceFail(self.request, self.permission_denied_message)


class InvoiceListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Invoice
    template_name = 'mvp/invoice/invoice_list.html'
    pk_url_kwarg = 'com_pk'
    ordering = ['id']
    permission_denied_message = f"Vous n'avez pas la permission de voir cette page."

    def get_queryset(self):
        if hasattr(self.request.user, 'manager'):
            return self.request.user.manager.company.invoice_set.all()
        else:
            return HttpResponseNotFound

    def test_func(self):
        return routeListDetailsInvoicePermissions(self, self.pk_url_kwarg)

    def handle_no_permission(self):
        return redirectWorkspaceFail(self.request, self.permission_denied_message)


class InvoiceDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Invoice
    template_name = 'mvp/invoice/invoice_details.html'
    pk_url_kwarg = 'invoice_pk'
    extra_context = {"button_update": "Update", "button_delete": "Delete"}
    permission_denied_message = f"Vous n'avez pas la permission de voir cette page."

    def get_queryset(self):
        # @TODO: Faire try except empty querryset ?
        return Invoice.objects.filter(pk=self.kwargs.get(self.pk_url_kwarg))

    def test_func(self):
        return routeListDetailsInvoicePermissions(self, self.pk_url_kwarg)

    def handle_no_permission(self):
        return redirectWorkspaceFail(self.request, self.permission_denied_message)


class InvoiceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Invoice
    template_name = 'mvp/invoice/invoice_details.html'
    object = None
    pk_url_kwarg = 'invoice_pk'
    extra_context = {"delete": True, "button": "Delete"}
    permission_denied_message = f"Vous n'avez pas la permission de voir cette page."

    def test_func(self):
        return routeCreateUpdateInvoicePermissions(self, self.kwargs.get('cpny_pk'),)

    def get_success_url(self):
        return reverse('mvp-invoice-list', args=[self.object.company.id, self.request.user.manager.id])

    def handle_no_permission(self):
        return redirectWorkspaceFail(self.request, self.permission_denied_message)
