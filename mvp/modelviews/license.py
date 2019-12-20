from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DeleteView

from mvp.controllers import redirectWorkspaceFail, FillConseilLicenseForm
from mvp.forms import LicenseForm
from mvp.models import License, Contract
from mvp.modelviews import permissions as perm


def CreateLicensePermissions(self, company_pk, contract_pk):
    if hasattr(self.request.user, 'manager'):
        manager = self.request.user.manager
        if manager.company.id == company_pk and (manager.role == 1 or manager.role == 2):
            return True
    elif hasattr(self.request.user, 'commercial'):
        contract = get_object_or_404(Contract, pk=contract_pk)
        commercial = self.request.user.commercial
        if not contract.validated and commercial.company.id == company_pk and commercial.id == contract.commercial.id:
            return True
    else:
        return False


def UpdateDeleteLicensePermissions(self, company_pk, contract_pk, license_pk):
    contract = get_object_or_404(Contract, pk=contract_pk)
    if hasattr(self.request.user, 'manager'):
        manager = self.request.user.manager
        if manager.company.id == company_pk and contract.company.id == manager.company.id \
                and (manager.role == 1 or manager.role == 2):
            return True
    elif hasattr(self.request.user, 'commercial'):
        license = get_object_or_404(License, pk=license_pk)
        if license.contract.validated:
            return False
        commercial = self.request.user.commercial
        if not contract.validated and commercial.company.id == company_pk \
                and commercial.id == license.contract.commercial.id:
            return True
    return False


class LicenseCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = License
    form_class = LicenseForm
    template_name = 'mvp/views/license_form.html'
    object = None
    pk_url_kwarg = 'contract_pk'
    extra_context = {"create_license": True, "button": "Ajouter une licence",
                     "page_title": "Easley - Create License", "page_heading": "Gestion des licences",
                     "section": "license", "content_heading": "Créer une licence"}
    permission_denied_message = perm.PERMISSION_DENIED
    success_message = f'Licence Créée !'

    def test_func(self):
        return CreateLicensePermissions(self, self.kwargs.get('cpny_pk'), self.kwargs.get(self.pk_url_kwarg))

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        args = [self.object.contract.company.id, self.object.contract.id]
        return reverse('mvp-contract-details', args=args)

    def get_form_kwargs(self, *args, **kwargs):
        return FillConseilLicenseForm(self, LicenseCreateView, *args, **kwargs)

    def handle_no_permission(self):
        return redirectWorkspaceFail(self.request, self.permission_denied_message)


class LicenseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = License
    form_class = LicenseForm
    template_name = 'mvp/views/license_form.html'
    object = None
    pk_url_kwarg = 'license_pk'
    extra_context = {"update_license": True, "button": "Modifier la licence",
                     "page_title": "Easley - Update License", "page_heading": "Gestion des licences",
                     "section": "license", "content_heading": "Modifier la licence"}
    permission_denied_message = perm.PERMISSION_DENIED
    success_message = f'Licence Modifiée'

    def test_func(self):
        return UpdateDeleteLicensePermissions(self,
            self.kwargs.get('cpny_pk'), self.kwargs.get('contract_pk'), self.kwargs.get(self.pk_url_kwarg))

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return self.object.get_absolute_url(self.object.contract.company.id, self.object.contract.id)

    def get_form_kwargs(self, *args, **kwargs):
        return FillConseilLicenseForm(self, LicenseUpdateView, *args, **kwargs)

    def handle_no_permission(self):
        return redirectWorkspaceFail(self.request, self.permission_denied_message)


# class LicenseDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
#     model = License
#     template_name = 'mvp/views/license_details.html'
#     pk_url_kwarg = 'license_pk'
#     extra_context = {"details": True,
#                      "page_title": "Easley - License Details", "page_heading": "Détail de la licence.",
#                      "section": "license", "content_heading": "Informations licence"}
#     permission_denied_message = PERMISSION_DENIED
#
#     def get_queryset(self):
#         return License.objects.filter(pk=self.kwargs.get(self.pk_url_kwarg))
#
#     def test_func(self):
#         cpny_pk = self.kwargs.get('cpny_pk')
#         if hasattr(self.request.user, 'manager'):
#             if self.request.user.manager.company.id == cpny_pk:
#                 return True
#         elif hasattr(self.request.user, 'commercial'):
#             licence = get_object_or_404(License, pk=self.kwargs.get(self.pk_url_kwarg))
#             commercial = self.request.user.commercial
#             if commercial.company.id == cpny_pk and commercial.id == licence.contract.commercial.id:
#                 return True
#         return False
#
#     def handle_no_permission(self):
#         return redirectWorkspaceFail(self.request, self.permission_denied_message)

@login_required
def LicenseDetails(request, cpny_pk=None, contract_pk=None, license_pk=None):
    context = {
        'content_heading': 'Détails de la licence.',
        'object': get_object_or_404(License, pk=license_pk)
    }
    contract = get_object_or_404(Contract, pk=contract_pk)

    if not contract.validated and request.method == "POST" and ('delete_license' in request.POST):
        context['object'].delete()
        return redirect('mvp-contract-details', cpny_pk=contract.company.id, contract_pk=contract.id)
    return render(request, 'mvp/views/license_details.html', context)


class LicenseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = License
    template_name = 'mvp/views/license_details.html'
    object = None
    pk_url_kwarg = 'license_pk'
    extra_context = {"delete_license": True,
                     "page_title": "Easley - Delete License", "page_heading": "Gestion des licenses",
                     "section": "license", "content_heading": "Supprimer une license"}
    permission_denied_message = perm.PERMISSION_DENIED
    success_message = f'Licence Supprimée !'

    def test_func(self):
        return UpdateDeleteLicensePermissions(self,
            self.kwargs.get('cpny_pk'), self.kwargs.get('contract_pk'), self.kwargs.get(self.pk_url_kwarg))

    def get_success_url(self):
        args = [self.object.contract.company.id, self.object.contract.id]
        messages.warning(self.request, self.success_message)
        return reverse('mvp-contract-details', args=args)

    def handle_no_permission(self):
        return redirectWorkspaceFail(self.request, self.permission_denied_message)


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
