from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseNotFound
from django.urls import reverse
from .models import Invoice, Contract
from .forms import InvoiceFrom, ContractForm
from .controllers import (
    validateCompanyInFormCreateUpdateView,
    routeCreateUpdateInvoicePermissions,
    routeListDetailsInvoicePermissions,
    redirectWorkspaceFail,
    FillConseilLicenseForm,
)

PERMISSION_DENIED = f"Oups, une erreur est survenue ! " \
                    f"Vous n'avez peut-être pas accès à cette page ou celle-ci n'existe plus."


class ContractUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Contract
    form_class = ContractForm
    template_name = 'mvp/views/contract_form.html'
    object = None
    pk_url_kwarg = 'contract_pk'
    extra_context = {"update_contract": True, "button": "Modifier le contrat",
                     "page_title": "Easley - Update Contract", "page_heading": "Modifier des contrats",
                     "section": "contract", "content_heading": "Modifier le contrat"}
    permission_denied_message = PERMISSION_DENIED
    success_message = f'Contrat Modifié'

    def test_func(self):
        # @ TODO: Faire permissions.
        return True

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return self.object.get_absolute_url(self.object.company.id)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ContractUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['client'] = kwargs['instance'].client
        kwargs['company'] = kwargs['instance'].company
        return kwargs

    def handle_no_permission(self):
        return redirectWorkspaceFail(self.request, self.permission_denied_message)


class InvoiceListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Invoice
    template_name = 'mvp/views/invoice_list.html'
    pk_url_kwarg = 'com_pk'
    ordering = ['contract__id']
    extra_context = {"list_invoice": True, "section": "invoice", }
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
        if self.object.licenses:
            context['licenses'] = self.object.licenses.all()
        if self.object.conseils:
            context['conseils'] = self.object.conseils.all()
        return context


# class InvoiceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
#     model = Invoice
#     template_name = 'mvp/views/invoice_details.html'
#     object = None
#     pk_url_kwarg = 'invoice_pk'
#     extra_context = {"delete_invoice": True,
#                      "page_title": "Easley - Delete Invoice", "page_heading": "Gestion des facture",
#                      "section": "invoice", "content_heading": "Supprimer une facture"}
#     permission_denied_message = PERMISSION_DENIED
#     success_message = f'Facture Supprimée !'
#
#     def test_func(self):
#         return routeCreateUpdateInvoicePermissions(self, self.kwargs.get('cpny_pk'), )
#
#     def get_success_url(self):
#         return reverse('mvp-invoice-list', args=[self.object.company.id, self.request.user.manager.id])
#
#     def handle_no_permission(self):
#         return redirectWorkspaceFail(self.request, self.permission_denied_message)
#
#
# class InvoiceCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
#     model = Invoice
#     form_class = InvoiceFrom
#     template_name = 'mvp/views/invoice_form.html'
#     object = None
#     pk_url_kwarg = 'cpny_pk'
#     extra_context = {"create_invoice": True, "button": "Ajouter une facture",
#                      "page_title": "Easley - Create Invoice", "page_heading": "Gestion des factures",
#                      "section": "invoice", "content_heading": "Créer une facture"}
#     permission_denied_message = PERMISSION_DENIED
#     success_message = f'Facture Créée !'
#
#     def form_valid(self, form):
#         return validateCompanyInFormCreateUpdateView(self, form)
#
#     def test_func(self):
#         return routeCreateUpdateInvoicePermissions(self, self.kwargs.get(self.pk_url_kwarg))
#
#     def get_success_url(self):
#         messages.success(self.request, self.success_message)
#         return self.object.get_absolute_url(self.object.company.id)
#
#     def get_form_kwargs(self, *args, **kwargs):
#         kwargs = super(InvoiceCreateView, self).get_form_kwargs()
#         kwargs['user'] = self.request.user
#         return kwargs
#
#     def handle_no_permission(self):
#         return redirectWorkspaceFail(self.request, self.permission_denied_message)
#
#
# class InvoiceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = Invoice
#     form_class = InvoiceFrom
#     template_name = 'mvp/views/invoice_form.html'
#     object = None
#     pk_url_kwarg = 'invoice_pk'
#     extra_context = {"update_invoice": True, "button": "Modifier une facture",
#                      "page_title": "Easley - Update Invoice", "page_heading": "Gestion des factures",
#                      "section": "invoice", "content_heading": "Modifier une facture"}
#     permission_denied_message = PERMISSION_DENIED
#     success_message = f'Facture Modifiée !'
#
#     def test_func(self):
#         return routeCreateUpdateInvoicePermissions(self, self.kwargs.get('cpny_pk'))
#
#     def get_success_url(self):
#         messages.success(self.request, self.success_message)
#         return self.object.get_absolute_url(self.object.company.id)
#
#     def get_form_kwargs(self, *args, **kwargs):
#         kwargs = super(InvoiceUpdateView, self).get_form_kwargs()
#         kwargs['user'] = self.request.user
#         return kwargs
#
#     def handle_no_permission(self):
#         return redirectWorkspaceFail(self.request, self.permission_denied_message)
#
