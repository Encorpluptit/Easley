from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ObjectDoesNotExist, EmptyResultSet, ValidationError
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.urls import reverse
from .models import Company, Commercial, Manager, Client, Conseil, License, Invoice, Contract
from .forms import ClientForm, ConseilForm, LicenseForm, InvoiceFrom
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

    def test_func(self):
        return routeCreatePermissions(self, self.kwargs.get(self.pk_url_kwarg), self.model)

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return self.object.get_absolute_url(self.object.company.id)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ClientCreateView, self).get_form_kwargs()
        if hasattr(self.request.user, 'manager'):
            kwargs['company'] = self.request.user.manager.company
            kwargs['manager'] = True
        elif hasattr(self.request.user, 'commercial'):
            kwargs['company'] = self.request.user.commercial.company
        kwargs['user'] = self.request.user
        return kwargs

    def handle_no_permission(self):
        return redirectWorkspaceFail(self.request, self.permission_denied_message)


# @ TODO: Refaire
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
        if hasattr(self.request.user, 'manager'):
            kwargs['company'] = self.request.user.manager.company
            kwargs['manager'] = True
        elif hasattr(self.request.user, 'commercial'):
            kwargs['company'] = self.request.user.commercial.company
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


# @ TODO: Refaire
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
        context['licenses'] = License.objects.filter(contract__client=self.object)
        context['conseils'] = Conseil.objects.filter(contract__client=self.object)
        return context


# @ TODO: Refaire
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


class ContractDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Contract
    template_name = 'mvp/views/contract_details.html'
    pk_url_kwarg = 'contract_pk'
    extra_context = {"details": True,
                     "page_title": "Easley - Contrat Details", "page_heading": "Gestion des Contrats",
                     "section": "contrat", "content_heading": "Détail Contrat"}
    permission_denied_message = PERMISSION_DENIED

    def get_queryset(self):
        return Contract.objects.filter(id=self.kwargs.get(self.pk_url_kwarg))

    def test_func(self):
        return routeDetailsPermissions(self, self.pk_url_kwarg, self.model)

    def handle_no_permission(self):
        return redirectWorkspaceFail(self.request, self.permission_denied_message)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['licenses'] = self.object.license_set.all()
        context['conseils'] = self.object.conseil_set.all()
        return context


class ConseilCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Conseil
    form_class = ConseilForm
    template_name = 'mvp/views/conseil_form.html'
    object = None
    pk_url_kwarg = 'contract_pk'
    extra_context = {"create_conseil": True, "button": "Ajouter un conseil",
                     "page_title": "Easley - Create Conseil", "page_heading": "Gestion des conseils",
                     "section": "conseil", "content_heading": "Créer un conseil"}
    permission_denied_message = PERMISSION_DENIED
    success_message = f'Conseil Créé !'

    def test_func(self):
        cpny_pk = self.kwargs.get('cpny_pk')
        if hasattr(self.request.user, 'manager'):
            manager = self.request.user.manager
            if manager.company.id == cpny_pk and (manager.role == 1 or manager.role == 2):
                return True
        elif hasattr(self.request.user, 'commercial'):
            contrat = get_object_or_404(Contract, pk=self.kwargs.get(self.pk_url_kwarg))
            commercial = self.request.user.commercial
            if commercial.company.id == cpny_pk and commercial.id == contrat.commercial.id:
                return True
        return False

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        # @ TODO: redirect vers views conseil details + form license ?
        return self.object.get_absolute_url(self.object.contract.company.id, self.object.contract.id)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ConseilCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        if hasattr(self.request.user, 'manager'):
            kwargs['company'] = self.request.user.manager.company
        elif hasattr(self.request.user, 'commercial'):
            kwargs['company'] = self.request.user.commercial.company
        kwargs['contract'] = get_object_or_404(Contract, pk=self.kwargs.get(self.pk_url_kwarg))
        return kwargs

    def handle_no_permission(self):
        return redirectWorkspaceFail(self.request, self.permission_denied_message)


# @ TODO: Refaire
class ConseilUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Conseil
    form_class = ConseilForm
    template_name = 'mvp/views/conseil_form.html'
    object = None
    pk_url_kwarg = 'conseil_pk'
    extra_context = {"update_conseil": True, "button": "Modifier le conseil",
                     "page_title": "Easley - Update Conseil", "page_heading": "Gestion des conseils.",
                     "section": "conseil", "content_heading": "Modifier le conseil."}
    permission_denied_message = PERMISSION_DENIED
    success_message = f'Conseil Modifié'

    def test_func(self):
        cpny_pk = self.kwargs.get('cpny_pk')
        if hasattr(self.request.user, 'manager'):
            manager = self.request.user.manager
            if manager.company.id == cpny_pk and manager.role == 1:
                return True
        elif hasattr(self.request.user, 'commercial'):
            contrat = get_object_or_404(Contract, pk=self.kwargs.get(self.pk_url_kwarg))
            commercial = self.request.user.commercial
            if commercial.company.id == cpny_pk and commercial.id == contrat.commercial.id:
                return True
        return False

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return self.object.get_absolute_url(self.object.company.id)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ConseilUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def handle_no_permission(self):
        return redirectWorkspaceFail(self.request, self.permission_denied_message)


# @ TODO: Refaire
class ConseilDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Conseil
    template_name = 'mvp/views/conseil_details.html'
    object = None
    pk_url_kwarg = 'conseil_pk'
    extra_context = {"delete_conseil": True,
                     "page_title": "Easley - Delete Conseil", "page_heading": "Gestion des conseils",
                     "section": "conseil", "content_heading": "Supprimer un conseil"}
    permission_denied_message = PERMISSION_DENIED
    success_message = f'Conseil Supprimé !'

    def test_func(self):
        return routeDeletePermissions(self, self.pk_url_kwarg, self.model)

    def get_success_url(self):
        if hasattr(self.request.user, 'commercial'):
            messages.warning(self.request, self.success_message)
            return reverse('mvp-conseil-list', args=[self.object.company.id, self.request.user.commercial.id])
        elif hasattr(self.request.user, 'manager'):
            messages.warning(self.request, self.success_message)
            return reverse('mvp-conseil-list', args=[self.object.company.id, self.request.user.manager.id])
        else:
            return redirectWorkspaceFail('mvp-workspace', self.success_message)

    def handle_no_permission(self):
        return redirectWorkspaceFail(self.request, self.permission_denied_message)


# @ TODO: A enlever ?
class LicenseCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = License
    form_class = LicenseForm
    template_name = 'mvp/views/license_form.html'
    object = None
    pk_url_kwarg = 'contract_pk'
    extra_context = {"create_license": True, "button": "Ajouter une license",
                     "page_title": "Easley - Create License", "page_heading": "Gestion des licenses",
                     "section": "license", "content_heading": "Créer une license"}
    permission_denied_message = PERMISSION_DENIED
    success_message = f'License Créée !'

    def test_func(self):
        cpny_pk = self.kwargs.get('cpny_pk')
        if hasattr(self.request.user, 'manager'):
            if self.request.user.manager.company.id == cpny_pk:
                return True
        elif hasattr(self.request.user, 'commercial'):
            contrat = get_object_or_404(Contract, pk=self.kwargs.get(self.pk_url_kwarg))
            commercial = self.request.user.commercial
            if commercial.company.id == cpny_pk and commercial.id == contrat.commercial.id:
                return True
        return False

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        args = [self.object.contract.company.id, self.object.contract.id]
        return reverse('mvp-contract-details', args=args)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(LicenseCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        if hasattr(self.request.user, 'manager'):
            kwargs['company'] = self.request.user.manager.company
        elif hasattr(self.request.user, 'commercial'):
            kwargs['company'] = self.request.user.commercial.company
        kwargs['contract'] = get_object_or_404(Contract, pk=self.kwargs.get(self.pk_url_kwarg))
        return kwargs

    def handle_no_permission(self):
        return redirectWorkspaceFail(self.request, self.permission_denied_message)


# @ TODO: Refaire
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
        cpny_pk = self.kwargs.get('cpny_pk')
        if hasattr(self.request.user, 'manager'):
            manager = self.request.user.manager
            if manager.company.id == cpny_pk and (manager.role == 1 or manager.role == 2):
                return True
        elif hasattr(self.request.user, 'commercial'):
            license = get_object_or_404(License, pk=self.kwargs.get(self.pk_url_kwarg))
            if license.contract.validated:
                return False
            commercial = self.request.user.commercial
            if commercial.company.id == cpny_pk and commercial.id == license.contract.commercial.id:
                return True
        return False

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return self.object.get_absolute_url(self.object.contract.company.id, self.object.contract.id)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(LicenseUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        if hasattr(self.request.user, 'manager'):
            kwargs['company'] = self.request.user.manager.company
        elif hasattr(self.request.user, 'commercial'):
            kwargs['company'] = self.request.user.commercial.company
        kwargs['contract'] = get_object_or_404(Contract, pk=self.kwargs.get('contract_pk'))
        return kwargs

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
        cpny_pk = self.kwargs.get('cpny_pk')
        if hasattr(self.request.user, 'manager'):
            manager = self.request.user.manager
            if manager.company.id == cpny_pk:
                return True
        elif hasattr(self.request.user, 'commercial'):
            license = get_object_or_404(License, pk=self.kwargs.get(self.pk_url_kwarg))
            commercial = self.request.user.commercial
            if commercial.company.id == cpny_pk and commercial.id == license.contract.commercial.id:
                return True
        return False

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
    template_name = 'mvp/views/invoice_form.html'
    object = None
    pk_url_kwarg = 'cpny_pk'
    extra_context = {"create_invoice": True, "button": "Ajouter une facture",
                     "page_title": "Easley - Create Invoice", "page_heading": "Gestion des factures",
                     "section": "invoice", "content_heading": "Créer une facture"}
    permission_denied_message = PERMISSION_DENIED
    success_message = f'Facture Créée !'

    def form_valid(self, form):
        return validateCompanyInFormCreateUpdateView(self, form)

    def test_func(self):
        return routeCreateUpdateInvoicePermissions(self, self.kwargs.get(self.pk_url_kwarg))

    def get_success_url(self):
        messages.success(self.request, self.success_message)
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
    template_name = 'mvp/views/invoice_form.html'
    object = None
    pk_url_kwarg = 'invoice_pk'
    extra_context = {"update_invoice": True, "button": "Modifier une facture",
                     "page_title": "Easley - Update Invoice", "page_heading": "Gestion des factures",
                     "section": "invoice", "content_heading": "Modifier une facture"}
    permission_denied_message = PERMISSION_DENIED
    success_message = f'Facture Modifiée !'

    def test_func(self):
        return routeCreateUpdateInvoicePermissions(self, self.kwargs.get('cpny_pk'))

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return self.object.get_absolute_url(self.object.company.id)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(InvoiceUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def handle_no_permission(self):
        return redirectWorkspaceFail(self.request, self.permission_denied_message)


class InvoiceListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Invoice
    template_name = 'mvp/views/invoice_list.html'
    pk_url_kwarg = 'com_pk'
    ordering = ['id']
    extra_context = {"list_invoice": True, "section": "invoice", }
    permission_denied_message = PERMISSION_DENIED

    def get_queryset(self):
        if hasattr(self.request.user, 'manager'):
            print(self.request.user.manager.company.invoice_set.all())
            return self.request.user.manager.company.invoice_set.all()
        else:
            return HttpResponseNotFound

    def test_func(self):
        return routeListDetailsInvoicePermissions(self, self.pk_url_kwarg)

    def handle_no_permission(self):
        return redirectWorkspaceFail(self.request, self.permission_denied_message)


class InvoiceDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Invoice
    template_name = 'mvp/views/invoice_details.html'
    pk_url_kwarg = 'invoice_pk'
    extra_context = {"details": True,
                     "page_title": "Easley - Invoice Details", "page_heading": "Gestion des factures",
                     "section": "invoice", "content_heading": "Informations factures"}
    permission_denied_message = PERMISSION_DENIED

    def get_queryset(self):
        return Invoice.objects.filter(pk=self.kwargs.get(self.pk_url_kwarg))

    def test_func(self):
        return routeListDetailsInvoicePermissions(self, self.pk_url_kwarg)

    def handle_no_permission(self):
        return redirectWorkspaceFail(self.request, self.permission_denied_message)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.license_set:
            context['licenses'] = self.object.license_set.all()
        if self.object.conseils:
            context['conseils'] = self.object.conseils.all()
        return context


class InvoiceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Invoice
    template_name = 'mvp/views/invoice_details.html'
    object = None
    pk_url_kwarg = 'invoice_pk'
    extra_context = {"delete_invoice": True,
                     "page_title": "Easley - Delete Invoice", "page_heading": "Gestion des facture",
                     "section": "invoice", "content_heading": "Supprimer une facture"}
    permission_denied_message = PERMISSION_DENIED
    success_message = f'Facture Supprimée !'

    def test_func(self):
        return routeCreateUpdateInvoicePermissions(self, self.kwargs.get('cpny_pk'), )

    def get_success_url(self):
        return reverse('mvp-invoice-list', args=[self.object.company.id, self.request.user.manager.id])

    def handle_no_permission(self):
        return redirectWorkspaceFail(self.request, self.permission_denied_message)


# class ConseilDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
#     model = Conseil
#     template_name = 'mvp/views/conseil_details.html'
#     pk_url_kwarg = 'conseil_pk'
#     extra_context = {"details": True,
#                      "page_title": "Easley - Conseil Details", "page_heading": "Gestion des conseils",
#                      "section": "conseil", "content_heading": "Informations conseil"}
#     permission_denied_message = PERMISSION_DENIED
#
#     def get_queryset(self):
#         return Conseil.objects.filter(id=self.kwargs.get(self.pk_url_kwarg))
#
#     def test_func(self):
#         cpny_pk = self.kwargs.get('cpny_pk')
#         if hasattr(self.request.user, 'manager'):
#             if self.request.user.manager.company.id == cpny_pk:
#                 return True
#         elif hasattr(self.request.user, 'commercial'):
#             contrat = get_object_or_404(Contract, pk=self.kwargs.get('contract_pk'))
#             commercial = self.request.user.commercial
#             if commercial.company.id == cpny_pk and commercial.id == contrat.commercial.id:
#                 return True
#         return False
#
#     def handle_no_permission(self):
#         return redirectWorkspaceFail(self.request, self.permission_denied_message)


# class ConseilListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
#     model = Conseil
#     template_name = 'mvp/views/conseil_list.html'
#     ordering = ['id']
#     pk_url_kwarg = 'com_pk'
#     extra_context = {"list_conseil": True, "section": "conseil", }
#     permission_denied_message = PERMISSION_DENIED
#
#     def get_queryset(self):
#         if hasattr(self.request.user, 'commercial'):
#             return self.request.user.commercial.conseil_set.all()
#         elif hasattr(self.request.user, 'manager'):
#             return self.request.user.manager.company.conseil_set.all()
#         else:
#             return HttpResponseNotFound
#
#     def test_func(self):
#         return routeListPermissions(self, self.pk_url_kwarg)
#
#     def handle_no_permission(self):
#         return redirectWorkspaceFail(self.request, self.permission_denied_message)


# class LicenseListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
#     model = License
#     template_name = 'mvp/views/license_list.html'
#     pk_url_kwarg = 'com_pk'
#     ordering = ['id']
#     extra_context = {"list_license": True, "section": "license", }
#     permission_denied_message = PERMISSION_DENIED
#
#     def get_queryset(self):
#         if hasattr(self.request.user, 'commercial'):
#             return self.request.user.commercial.license_set.all()
#         elif hasattr(self.request.user, 'manager'):
#             return self.request.user.manager.company.license_set.all()
#         else:
#             return HttpResponseNotFound
#
#     def test_func(self):
#         return routeListPermissions(self, self.pk_url_kwarg)
#
#     def handle_no_permission(self):
#         return redirectWorkspaceFail(self.request, self.permission_denied_message)
