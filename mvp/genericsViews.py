from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Client, Service, Commercial, License
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import ServiceRegisterForm


# class ClientListView(ListView):
class ClientListView(ListView):
    model = Client
    template_name = 'mvp/clients/client_list.html'
    # context_object_name = 'client_list'
    ordering = ['id']

    def get_queryset(self):
        # if hasattr(self.request.user, 'commercial'):
        #     return Client.objects.filter(commercial=self.request.user.commercial)
        # if hasattr(self.request.user, 'ceo'):
        #     return Client.objects.filter(company=self.request.user.ceo.company)
        return Client.objects.filter(company=self.request.user.commercial.company)


class ClientDetailView(DetailView):
    model = Client
    template_name = 'mvp/clients/client_details.html'


# class ServiceListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
class ServiceListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Service
    template_name = 'mvp/service/service_list.html'
    # context_object_name = 'service_list'
    ordering = ['id']

    def get_queryset(self):
        commercial = get_object_or_404(Commercial, pk=self.kwargs.get('com_pk'))
        return Service.objects.filter(commercial=commercial)

    def test_func(self):
        commercial = get_object_or_404(Commercial, user=self.request.user)
        if commercial.id == self.kwargs.get('com_pk'):
            return True
        return False


class ServiceDetailView(DetailView):
    model = Service
    template_name = 'mvp/service/service_details.html'

    def get_queryset(self):
        return Service.objects.filter(pk=self.kwargs.get('pk'))


# @TODO: A modifier
class ServiceUpdateView(UpdateView):
    model = Service
    fields = '__all__'
    template_name = 'mvp/forms/service_form.html'

    def get_queryset(self):
        return Service.objects.filter(pk=self.kwargs.get('pk'))


class LicenseListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = License
    template_name = 'mvp/license/license_list.html'
    # context_object_name = 'service_list'
    ordering = ['id']

    def get_queryset(self):
        commercial = get_object_or_404(Commercial, pk=self.kwargs.get('com_pk'))
        return License.objects.filter(commercial=commercial)

    def test_func(self):
        commercial = get_object_or_404(Commercial, user=self.request.user)
        if commercial.id == self.kwargs.get('com_pk'):
            return True
        return False


class LicenseDetailView(DetailView):
    model = License
    template_name = 'mvp/license/license_details.html'

    def get_queryset(self):
        return License.objects.filter(pk=self.kwargs.get('pk'))


class ClientCreateView(CreateView):
    # @TODO: Changer class form directement dans le HTML pour utiliser ça.
    model = Client
    fields = ['name', 'email', ]
    template_name = 'mvp/forms/client_form.html'

    def form_valid(self, form):
        form.instance.commercial = self.request.user.commercial or self.request.user.ceo
        form.instance.company = self.request.user.commercial.company or self.request.user.ceo.company
        return super().form_valid(form)
