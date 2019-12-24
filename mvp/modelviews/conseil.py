from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import CreateView, UpdateView

from mvp.controllers import (
    redirectWorkspaceFail,
    FillConseilLicenseForm,
    createExcelServices,
)
from mvp.forms import ConseilForm, ServiceForm
from mvp.models import Conseil, Contract, Service
from mvp.modelviews import permissions as perm


class ConseilCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Conseil
    form_class = ConseilForm
    template_name = 'mvp/views/conseil_form.html'
    object = None
    pk_url_kwarg = 'contract_pk'
    extra_context = {"create_conseil": True, "button": "Ajouter un conseil",
                     "page_title": "Easley - Create Conseil", "page_heading": "Gestion des conseils",
                     "section": "conseil", "content_heading": "Créer un conseil"}
    permission_denied_message = perm.PERMISSION_DENIED
    success_message = f'Conseil Créé !'

    def test_func(self):
        contract = get_object_or_404(Contract, pk=self.kwargs.get(self.pk_url_kwarg))
        return perm.createConseilLicense(self.request.user, contract)

    def form_valid(self, form):
        form.instance.save()
        createExcelServices(form)
        form.instance.save(update_fields=['price', ])
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return self.object.get_absolute_url(self.object.contract.company.id, self.object.contract.id)

    def get_form_kwargs(self, *args, **kwargs):
        return FillConseilLicenseForm(self, ConseilCreateView, *args, **kwargs)

    def handle_no_permission(self):
        return redirectWorkspaceFail(self.request, self.permission_denied_message)


class ConseilUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Conseil
    form_class = ConseilForm
    template_name = 'mvp/views/conseil_form.html'
    object = None
    pk_url_kwarg = 'conseil_pk'
    extra_context = {"update_conseil": True, "button": "Modifier le conseil",
                     "page_title": "Easley - Update Conseil", "page_heading": "Gestion des conseils.",
                     "section": "conseil", "content_heading": "Modifier le conseil."}
    permission_denied_message = perm.PERMISSION_DENIED
    success_message = f'Conseil Modifié'

    def test_func(self):
        contract = get_object_or_404(Contract, pk=self.kwargs.get('contract_pk'))
        return perm.updateConseilLicense(self.request.user, contract, self.get_object())

    def form_valid(self, form):
        createExcelServices(form)
        if 'price' in form.changed_data:
            form.instance.save(update_fields=['price', ])
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return self.object.get_absolute_url(self.object.company.id, self.object.contract.id)

    def get_form_kwargs(self, *args, **kwargs):
        return FillConseilLicenseForm(self, ConseilUpdateView, *args, **kwargs)

    def handle_no_permission(self):
        return redirectWorkspaceFail(self.request, self.permission_denied_message)


# @ TODO: Faire permissions, faire la gestion du changement d'excel
@login_required
def ConseilDetails(request, cpny_pk=None, contract_pk=None, conseil_pk=None):
    context = {
        'content_heading': 'Rentrer les informations nécessaires à la création du conseil.',
        'object': get_object_or_404(Conseil, pk=conseil_pk),
    }
    contract = get_object_or_404(Contract, pk=contract_pk)
    context['services'] = context['object'].service_set.all() or None

    serviceForm = ServiceForm(request.POST or None, user=request.user, company=contract.company, conseil=context['object'])
    if request.method == "POST":
        print(request.POST)
        if ('delete_conseil' in request.POST):
            context['object'].delete()
            return redirect('mvp-contract-details', cpny_pk=contract.company.id, contract_pk=contract.id)
        elif ('delete_service' in request.POST) and ('service_id_delete' in request.POST):
            service = get_object_or_404(Service, id=request.POST['service_id_delete'])
            service.delete()
        elif 'never_end' in request.POST and 'service_id_end' in request.POST:
            service = context['services'].get(id=request.POST['service_id_end'])
            service.done = True
            service.save()
        elif 'end_date' in request.POST and 'service_id' in request.POST and request.POST['end_date'] != '':
            service = context['services'].get(id=request.POST['service_id'])
            service.actual_date = datetime.strptime(request.POST['end_date'], '%d/%m/%Y').date()
            service.done = True
            service.save()
        elif serviceForm.is_valid():
            service = serviceForm.save()
            service.conseil.save(update_fields=['price', ])
    if contract.validated:
        context['content_heading'] = 'Détails du conseil'
    context['services'] = context['object'].service_set.all() or None
    context['serviceForm'] = serviceForm
    return render(request, 'mvp/views/conseil_details.html', context)


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

