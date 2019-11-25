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

PERMISSION_DENIED = f"Oups, une erreur est survenue ! " \
                    f"Vous n'avez peut-être pas accès à cette page ou celle-ci n'existe plus."

class ClientCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'mvp/views/client_form.html'
    object = None
    pk_url_kwarg = 'cpny_pk'
    extra_context = {"create_client": True, "button": "Ajouter un client",
                     "page_title": "Easley - Create Client", "page_heading": "Gestion des clients",
                     "section": "client", "content_heading": "Créer un client"}
    permission_denied_message = PERMISSION_DENIED
    success_message = f'Client Créé !'

    def form_valid(self, form):
        return validateCompanyInFormCreateUpdateView(self, form)

    def test_func(self):
        return routeCreatePermissions(self, self.kwargs.get(self.pk_url_kwarg), self.model)

    def get_success_url(self):
        messages.success(self.request, self.success_message)
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
    template_name = 'mvp/views/client_form.html'
    object = None
    pk_url_kwarg = 'client_pk'
    extra_context = {"update_client": True, "button": "Modifier le client",
                     "page_title": "Easley - Update Client", "page_heading": "Gestion des clients",
                     "section": "client", "content_heading": "Modifier un client"}
    permission_denied_message = PERMISSION_DENIED
    success_message = f'Client Modifié !'

    def test_func(self):
        return routeUpdatePermissions(self, self.pk_url_kwarg, self.model)

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return self.object.get_absolute_url(self.object.company.id)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ClientUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def handle_no_permission(self):
        return redirectWorkspaceFail(self.request, self.permission_denied_message)


class ClientListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Client
    template_name = 'mvp/views/client_list.html'
    ordering = ['id']
    pk_url_kwarg = 'com_pk'
    # @ TODO: Rajouter list_client_info (pour list client delete ??)
    extra_context = {"list_client": True, "section": "client", }
    permission_denied_message = PERMISSION_DENIED

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
    template_name = 'mvp/views/client_details.html'
    pk_url_kwarg = 'client_pk'
    extra_context = {"details": True,
                     "page_title": "Easley - Client Details", "page_heading": "Gestion des clients",
                     "section": "client", "content_heading": "Informations client"}
    permission_denied_message = PERMISSION_DENIED

    def get_queryset(self):
        return Client.objects.filter(id=self.kwargs.get(self.pk_url_kwarg))

    def test_func(self):
        return routeDetailsPermissions(self, self.pk_url_kwarg, self.model)

    def handle_no_permission(self):
        return redirectWorkspaceFail(self.request, self.permission_denied_message)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['licenses'] = self.object.license_set.all()
        context['services'] = self.object.service_set.all()
        return context


class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Client
    template_name = 'mvp/views/client_details.html'
    object = None
    pk_url_kwarg = 'client_pk'
    extra_context = {"delete_client": True,
                     "page_title": "Easley - Delete Client", "page_heading": "Gestion des clients",
                     "section": "client", "content_heading": "Supprimer un client"}
    permission_denied_message = PERMISSION_DENIED
    success_message = f'Client Supprimé !'

    def test_func(self):
        return routeDeletePermissions(self, self.pk_url_kwarg, self.model)

    def get_success_url(self):
        if hasattr(self.request.user, 'commercial'):
            messages.warning(self.request, self.success_message)
            return reverse('mvp-client-list', args=[self.object.company.id, self.request.user.commercial.id])
        elif hasattr(self.request.user, 'manager'):
            messages.warning(self.request, self.success_message)
            return reverse('mvp-client-list', args=[self.object.company.id, self.request.user.manager.id])
        else:
            redirectWorkspaceFail(self.request, self.success_message)

    def handle_no_permission(self):
        return redirectWorkspaceFail(self.request, self.permission_denied_message)


class ServiceCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'mvp/service/service_form.html'
    object = None
    pk_url_kwarg = 'cpny_pk'
    extra_context = {"button": "Ajouter un Service"}
    permission_denied_message = PERMISSION_DENIED

    def form_valid(self, form):
        # print(form.cleaned_data)
        # self.request.session['service_form_data'] = form.cleaned_data
        return validateCompanyInFormCreateUpdateView(self, form)

    def test_func(self):
        return routeCreatePermissions(self, self.kwargs.get(self.pk_url_kwarg), self.model)

    def get_success_url(self):
        return self.object.get_absolute_url(self.object.company.id)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ServiceCreateView, self).get_form_kwargs()
        # kwargs = {'data': self.request.session.get('service_form_data', None)}
        # kwargs.update(super(ServiceCreateView, self).get_form_kwargs())
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
    permission_denied_message = PERMISSION_DENIED

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
    permission_denied_message = PERMISSION_DENIED

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
    permission_denied_message = PERMISSION_DENIED

    def get_queryset(self):
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
    permission_denied_message = PERMISSION_DENIED

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
    template_name = 'mvp/views/license_form.html'
    object = None
    pk_url_kwarg = 'cpny_pk'
    extra_context = {"create_license": True, "button": "Ajouter une license",
                     "page_title": "Easley - Create License", "page_heading": "Gestion des licenses",
                     "section": "license", "content_heading": "Créer une license"}
    permission_denied_message = PERMISSION_DENIED
    success_message = f'License Créée !'

    def form_valid(self, form):
        # print(form.cleaned_data)
        self.request.session['license_form_data'] = form.cleaned_data
        return validateCompanyInFormCreateUpdateView(self, form)

    def test_func(self):
        return routeCreatePermissions(self, self.kwargs.get(self.pk_url_kwarg), self.model)

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return self.object.get_absolute_url(self.object.company.id)

    def get_form_kwargs(self, *args, **kwargs):
        # del self.request.session['license_form_data']
        print("session in get_form kwargs", self.request.session.get('license_form_data', None))
        kwargs = {'data': self.request.session.get('license_form_data', None)}
        kwargs.update(super(LicenseCreateView, self).get_form_kwargs())
        # kwargs = super(LicenseCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        print(kwargs)
        return kwargs

    def handle_no_permission(self):
        return redirectWorkspaceFail(self.request, self.permission_denied_message)


class LicenseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = License
    form_class = LicenseForm
    template_name = 'mvp/views/license_form.html'
    object = None
    pk_url_kwarg = 'license_pk'
    extra_context = {"update_license": True, "button": "Modifier la license",
                     "page_title": "Easley - Update License", "page_heading": "Gestion des licenses",
                     "section": "license", "content_heading": "Modifier la license"}
    permission_denied_message = PERMISSION_DENIED
    success_message = f'License Modifiée'

    def test_func(self):
        return routeUpdatePermissions(self, self.pk_url_kwarg, self.model)

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return self.object.get_absolute_url(self.object.company.id)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(LicenseUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def handle_no_permission(self):
        return redirectWorkspaceFail(self.request, self.permission_denied_message)


class LicenseListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = License
    template_name = 'mvp/views/license_list.html'
    pk_url_kwarg = 'com_pk'
    ordering = ['id']
    extra_context = {"list_license": True, "section": "license",}
    permission_denied_message = PERMISSION_DENIED

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
    template_name = 'mvp/views/license_details.html'
    pk_url_kwarg = 'license_pk'
    extra_context = {"details": True,
                     "page_title": "Easley - License Details", "page_heading": "Gestion des licenses",
                     "section": "license", "content_heading": "Informations license"}
    permission_denied_message = PERMISSION_DENIED

    def get_queryset(self):
        return License.objects.filter(pk=self.kwargs.get(self.pk_url_kwarg))

    def test_func(self):
        return routeDetailsPermissions(self, self.pk_url_kwarg, self.model)

    def handle_no_permission(self):
        return redirectWorkspaceFail(self.request, self.permission_denied_message)


class LicenseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = License
    template_name = 'mvp/views/license_details.html'
    object = None
    pk_url_kwarg = 'license_pk'
    extra_context = {"delete_license": True,
                     "page_title": "Easley - Delete License", "page_heading": "Gestion des licenses",
                     "section": "license", "content_heading": "Supprimer une license"}
    permission_denied_message = PERMISSION_DENIED
    success_message = f'License Supprimée !'

    def test_func(self):
        return routeDeletePermissions(self, self.pk_url_kwarg, self.model)

    def get_success_url(self):
        if hasattr(self.request.user, 'commercial'):
            messages.warning(self.request, self.success_message)
            return reverse('mvp-license-list', args=[self.object.company.id, self.request.user.commercial.id])
        elif hasattr(self.request.user, 'manager'):
            messages.warning(self.request, self.success_message)
            return reverse('mvp-license-list', args=[self.object.company.id, self.request.user.manager.id])
        else:
            return redirectWorkspaceFail(self.request, self.success_message)

    def handle_no_permission(self):
        return redirectWorkspaceFail(self.request, self.permission_denied_message)


class InvoiceCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Invoice
    form_class = InvoiceFrom
    template_name = 'mvp/invoice/invoice_form.html'
    object = None
    pk_url_kwarg = 'cpny_pk'
    extra_context = {"button": "Ajouter une facture"}
    permission_denied_message = PERMISSION_DENIED

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
    permission_denied_message = PERMISSION_DENIED

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
    permission_denied_message = PERMISSION_DENIED

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
    permission_denied_message = PERMISSION_DENIED

    def get_queryset(self):
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
    permission_denied_message = PERMISSION_DENIED

    def test_func(self):
        return routeCreateUpdateInvoicePermissions(self, self.kwargs.get('cpny_pk'), )

    def get_success_url(self):
        return reverse('mvp-invoice-list', args=[self.object.company.id, self.request.user.manager.id])

    def handle_no_permission(self):
        return redirectWorkspaceFail(self.request, self.permission_denied_message)
