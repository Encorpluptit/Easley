from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from .models import Company, Commercial, Manager, Client, Service, License
from .forms import ServiceForm, ClientForm
from .controllers import routeListPermissions, routeDetailsPermissions


class ClientListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Client
    template_name = 'mvp/clients/client_list.html'
    ordering = ['id']
    pk_url_kwarg = 'com_pk'

    def get_queryset(self):
        try:
            return Client.objects.filter(commercial=self.request.user.commercial)
        except ObjectDoesNotExist:
            return Client.objects.filter(company=self.request.user.manager.company)
        # @TODO: RAISE ERROR 404

    def test_func(self):
        return routeListPermissions(self, self.pk_url_kwarg)


class ClientDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Client
    template_name = 'mvp/clients/client_details.html'
    pk_url_kwarg = 'client_pk'

    def get_queryset(self):
        return Client.objects.filter(id=self.kwargs.get(self.pk_url_kwarg))

    def test_func(self):
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


class ServiceDetailView(DetailView):
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
        return routeDetailsPermissions(self, self.pk_url_kwarg, self.model)


class LicenseDetailView(DetailView):
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


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'mvp/forms/client_form.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.user)
        form.save()

    def form_valid(self, form):
        # print(self.request)
        # form.instance.commercial = self.request.user.commercial or self.request.user.manager
        # form.instance.company = self.request.user.commercial.company or self.request.user.manager.company
        return super().form_valid(form)


