from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from dateutil.relativedelta import relativedelta
from dateutil.utils import today
from django.db.models import Sum
from .models import Company, Commercial, Manager, Client, Conseil, License, Contract, Invoice
from .controllers import customRegisterUser, CreateAllInvoice
from .forms import (
    UserRegisterForm,
    CompanyForm,
    ContractForm,
    ClientForm,
    ServiceForm,
)


# Create your views here.


def home(request):
    return render(request, 'mvp/misc/home.html')


def about(request):
    return render(request, 'mvp/misc/about.html')


def contact(request):
    return render(request, 'mvp/misc/contact.html')


def register(request):
    form = UserRegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        if customRegisterUser(request, form):
            return redirect('mvp-join-company')
        else:
            return redirect(request, 'mvp-home')
    return render(request, 'mvp/misc/register.html', {'form': form})


# @ TODO: A Refaire avec CreateView ? OUI
@login_required
def companyCreation(request):
    form = CompanyForm(request.POST or None, ceo=request.user)
    if request.method == "POST" and form.is_valid():
        try:
            company = form.save()
            ceo = Manager.objects.create(user=request.user, company=company, role=1)
            ceo.save()
            messages.success(request, f'Company {company.name} Created, Welcome {ceo} !')
        except:
            messages.warning(request, f'An Error occurred ! Please try again later')
        return redirect('mvp-home')
    return render(request, 'mvp/misc/company_creation.html', {'form': form})


# @ TODO: Faire permissions
@login_required
def CreateContractClient(request, **kwargs):
    context = {
        'page': 'contract_client',
        'post': False,
    }
    company, manager = None, False

    if hasattr(request.user, 'commercial'):
        context['client_list'] = request.user.commercial.client_set.all()
        company = request.user.commercial.company
    if hasattr(request.user, 'manager'):
        context['client_list'] = request.user.manager.company.client_set.all()
        company = request.user.manager.company
        manager = True
    form = ClientForm(request.POST or None, user=request.user, company=company, manager=manager)
    if request.method == "POST":
        context['post'] = True
        if form.is_valid():
            client = form.save()
            messages.success(request, f'Client créé.')
            return redirect('mvp-contract-form', company.id, client.id)
    context['form'] = form
    return render(request, 'mvp/views/contract_client.html', context)


# @ TODO: Faire permissions
@login_required
def CreateContractForm(request, cpny_pk=None, client_pk=None):
    client = get_object_or_404(Client, pk=client_pk)
    company = get_object_or_404(Company, pk=cpny_pk)
    form = ContractForm(request.POST or None, user=request.user, client=client, company=company)
    form.fields['commercial'].initial = client.commercial.id
    if request.method == "POST":
        if form.is_valid():
            contract = form.save(commit=False)
            contract.save()
            messages.success(request, f'Contrat créé.')
            return redirect('mvp-contract-details', company.id, contract.id, )
    return render(request, 'mvp/views/contract_form.html', {'form': form})


# @ TODO: Faire permissions


@login_required
def ContractDetails(request, cpny_pk=None, contract_pk=None, conseil_pk=None):
    context = {
        "page_title": "Easley - Contrat Details", "page_heading": "Gestion des Contrats",
        "section": "contrat", "content_heading": "Détail Contrat"
    }
    contract = get_object_or_404(Contract, pk=contract_pk)
    conseils = contract.conseil_set.all()
    licenses = contract.license_set.all()

    context['object'] = contract
    context['licenses'] = licenses
    context['conseils'] = conseils
    context['progression'] = 0
    date_now = today().date()
    if contract.start_date <= date_now:
        try:
            context['progression'] = int((date_now - contract.start_date) / (contract.end_date - contract.start_date) * 100)
        except ZeroDivisionError:
            pass
    if contract.validated:
        return render(request, 'mvp/views/contract_details.html', context)
    if request.method == "POST" and not contract.validated:
        if conseils.count() <= 0 and licenses.count() <= 0:
            messages.info(request, f"Le contrat est vide. Veuillez rentrer une license ou un conseil.")
        else:
            CreateAllInvoice(contract, licenses, conseils)
            contract.validated = True
            contract.save()
            messages.success(request, f'Contrat Validé.')
            return redirect(contract.get_absolute_url(contract.company.id))
    return render(request, 'mvp/views/contract_details.html', context)


# @ TODO: A refaire (avec BaseView ?) pour fichier de services / Faire permissions
@login_required
def ConseilDetails(request, cpny_pk=None, contract_pk=None, conseil_pk=None):
    context = {
        'content_heading': 'Rentrer les informations nécessaires à la création du conseil.',
        'object': get_object_or_404(Conseil, pk=conseil_pk)
    }
    contract = get_object_or_404(Contract, pk=contract_pk)

    if contract.validated:
        context['content_heading'] = 'Détails du conseil'
        return render(request, 'mvp/views/conseil_details.html', context)
    company = get_object_or_404(Company, pk=cpny_pk)
    form = ServiceForm(request.POST or None, user=request.user, company=company, conseil=context['object'])
    if request.method == "POST" and form.is_valid():
        form.save()
        return render(request, 'mvp/views/conseil_details.html', context)
    context['form'] = form
    return render(request, 'mvp/views/conseil_details.html', context)


def ContractListView(request, cpny_pk=None):
    context = {'validated_contracts': None}
    if hasattr(request.user, 'commercial'):
        contracts = request.user.commercial.contract_set.all()
        context['validated_contracts'] = contracts.filter(validated=True)
        context['not_validated_contracts'] = contracts.filter(validated=False)
    elif hasattr(request.user, 'manager'):
        contracts = request.user.manager.company.contract_set.all()
        context['validated_contracts'] = contracts.filter(validated=True)
        context['not_validated_contracts'] = contracts.filter(validated=False)
    return render(request, 'mvp/views/contract_list.html', context)


@login_required
def join_company(request):
    if request.method == "POST":
        try:
            company = Company.objects.get(pk=int(request.POST['company_id']))
            Commercial.objects.create(user=request.user, company=company)
            return redirect('mvp-commercial-workspace')
        except:
            messages.warning(request, f'Wrong company ID')
    return render(request, 'mvp/misc/join_company.html')


@login_required
def commercialWorkspace(request):
    return render(request, 'mvp/workspace/bizdev.html')


@login_required
def ceoWorkspace(request):
    return render(request, 'mvp/workspace/manager.html')


@login_required
def workspace(request):
    if hasattr(request.user, 'commercial'):
        return redirect('mvp-commercial-workspace')
    elif hasattr(request.user, 'manager'):
        return redirect('mvp-manager-workspace')
    else:
        return redirect('mvp-join-company')

# @login_required
# def serviceCreation(request):
#     form = ConseilForm(request.POST or None, user=request.user)
#     # print(request.POST)
#     if request.method == "POST" and form.is_valid():
#         if hasattr(request.user, 'commercial'):
#             # clean_form = form.save(commit=False)
#             # clean_form.company = request.user.commercial.company
#             # clean_form.commercial = request.user.commercial
#             form.save()
#             messages.success(request, f'service created!')
#             return redirect('mvp-workspace')
#         elif hasattr(request.user, 'manager'):
#             # clean_form = form.save(commit=False)
#             # clean_form.company = request.user.manager.company
#             form.save()
#             messages.success(request, f'service created!')
#             return redirect('mvp-workspace')
#     return render(request, 'mvp/service/service_form.html', {'form': form})
#
#
# @login_required
# def licenseCreation(request):
#     form = LicenseForm(request.POST or None, user=request.user)
#     if request.method == "POST" and form.is_valid():
#         if hasattr(request.user, 'commercial'):
#             clean_form = form.save(commit=False)
#             clean_form.company = request.user.commercial.company
#             clean_form.commercial = request.user.commercial
#             form.save()
#             messages.success(request, f'license created!')
#             return redirect('mvp-workspace')
#     return render(request, 'mvp/license/license_form.html', {'form': form})


# class ContractDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
#     model = Contract
#     template_name = 'mvp/views/contract_details.html'
#     pk_url_kwarg = 'contract_pk'
#     extra_context = {"details": True,
#                      "page_title": "Easley - Contrat Details", "page_heading": "Gestion des Contrats",
#                      "section": "contrat", "content_heading": "Détail Contrat"}
#     permission_denied_message = PERMISSION_DENIED
#
#     def get_queryset(self):
#         return Contract.objects.filter(id=self.kwargs.get(self.pk_url_kwarg))
#
#     def test_func(self):
#         return routeDetailsPermissions(self, self.pk_url_kwarg, self.model)
#
#     def handle_no_permission(self):
#         return redirectWorkspaceFail(self.request, self.permission_denied_message)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['licenses'] = self.object.license_set.all()
#         context['conseils'] = self.object.conseil_set.all()
#         return context


# @login_required
# def LicenseUpdate(request,  cpny_pk=None, contract_pk=None, license_pk=None):
#     context = {
#         'content_heading': 'Modifier la license.',
#     }
#     license = get_object_or_404(License, pk=license_pk)
#     contract = license.contract
#     form = LicenseForm(instance=license, company=contract.company, contract=contract)
#     # form.fields['duration'].initial = license.duration
#     print(request.POST, form.is_valid())
#     if request.method == "POST" and form.is_valid():
#         new_license = form.save()
#         contract.price += (new_license.price - license.price)
#         print("VALID")
#         contract.save()
#         return redirect('mvp-license-details', contract.company.id, contract.id, license.id)
#     context['form'] = form
#     return render(request, 'mvp/views/license_form.html', context)
