from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView

from mvp.forms import ClientForm
from mvp.models import Client, License, Conseil, Manager, Commercial
from mvp.modelviews import PERMISSION_DENIED
from mvp.controllers import (
    redirectWorkspaceFail,
    routeListPermissions,
    routeDetailsPermissions,
)


def CreateClientPermissions(self, company_pk):
    try:
        manager = Manager.objects.get(user=self.request.user)
        if manager.company.id == company_pk:
            if manager.role == 3:
                return False
            return True
    except ObjectDoesNotExist:
        commercial = get_object_or_404(Commercial, user=self.request.user)
        if commercial.company.id == company_pk:
            return True
        else:
            return False


def UpdateClientPermissions(self, company_pk, client_pk):
    client = get_object_or_404(Client, pk=client_pk)
    try:
        manager = Manager.objects.get(user=self.request.user)
        if manager.company.id == company_pk and client.company.id == manager.company.id:
            if manager.role == 3:
                return False
            return True
    except ObjectDoesNotExist:
        commercial = get_object_or_404(Commercial, user=self.request.user)
        if commercial.company.id == company_pk and client.commercial.id == commercial.id:
            return True
        else:
            return False


def DeleteClientPermissions(self, company_pk, client_pk):
    client = get_object_or_404(Client, pk=client_pk)
    try:
        manager = Manager.objects.get(user=self.request.user)
        if manager.company.id == company_pk and client.company.id == manager.company.id:
            if manager.role == 3:
                return False
            return True
    except ObjectDoesNotExist:
        return False


def FillClientFormKwarg(self, model_view, *args, **kwargs):
    kwargs = super(model_view, self).get_form_kwargs()
    if hasattr(self.request.user, 'manager'):
        kwargs['company'] = self.request.user.manager.company
        kwargs['manager'] = True
    elif hasattr(self.request.user, 'commercial'):
        kwargs['company'] = self.request.user.commercial.company
    kwargs['user'] = self.request.user
    return kwargs


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
        return CreateClientPermissions(self, self.kwargs.get(self.pk_url_kwarg))
        # return routeCreatePermissions(self, self.kwargs.get(self.pk_url_kwarg), self.model)

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return self.object.get_absolute_url(self.object.company.id)

    def get_form_kwargs(self, *args, **kwargs):
        return FillClientFormKwarg(self, ClientCreateView, *args, **kwargs)

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
        return UpdateClientPermissions(self, self.kwargs.get('cpny_pk'), self.kwargs.get(self.pk_url_kwarg))
        # return routeUpdatePermissions(self, self.pk_url_kwarg, self.model)

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return self.object.get_absolute_url(self.object.company.id)

    def get_form_kwargs(self, *args, **kwargs):
        return FillClientFormKwarg(self, ClientUpdateView, *args, **kwargs)

    def handle_no_permission(self):
        return redirectWorkspaceFail(self.request, self.permission_denied_message)


class ClientListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Client
    template_name = 'mvp/views/client_list.html'
    ordering = ['id']
    pk_url_kwarg = 'com_pk'
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
        context['licenses'] = License.objects.filter(contract__client=self.object)
        context['conseils'] = Conseil.objects.filter(contract__client=self.object)
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
        return DeleteClientPermissions(self, self.kwargs.get('cpny_pk'), self.kwargs.get(self.pk_url_kwarg))

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