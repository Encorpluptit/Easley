from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Company, Commercial, Manager, Client, Conseil, License, Contract
from .controllers import customRegisterUser, customCompanyRegister
from .forms import (
    UserRegisterForm,
    CompanyForm,
    ClientForm,
    UserUpdateForm,
    ConseilForm,
    LicenseForm,
    ContractForm,
    ClientContractForm,
)
from django.urls import reverse


# Create your views here.


def home(request):
    return render(request, 'mvp/misc/home.html')


def about(request):
    return render(request, 'mvp/misc/about.html')


def contact(request):
    return render(request, 'mvp/base/contact.html')


# @ TODO: A Refaire avec CreateView ?
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
        customCompanyRegister(request, form)
        return redirect('mvp-home')
    return render(request, 'mvp/misc/company_creation.html', {'form': form})


# @ TODO: Faire permissions
@login_required
def CreateContract_Client(request, **kwargs):
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
    form = ClientContractForm(request.POST or None, user=request.user, company=company, manager=manager)
    if request.method == "POST":
        context['post'] = True
        if form.is_valid():
            client = form.save()
            request.session['company'] = company
            request.session['client'] = client
            messages.success(request, f'Client créé.')
            return redirect('mvp-contract-form', company.id, client.id)
    context['form'] = form
    return render(request, 'mvp/views/contract_client.html', context)

# @ TODO: Faire permissions
@login_required
def CreateContract_Contract(request, cpny_pk=None, client_pk=None):
    if 'client' in request.session and 'company' in request.session:
        client = request.session.get('client', None)
        company = request.session.get('company', None)
    else:
        client = get_object_or_404(Client, pk=client_pk)
        company = get_object_or_404(Company, pk=cpny_pk)
    form = ContractForm(request.POST or None, user=request.user, client=client, company=company)
    if request.method == "POST":
        print(request.POST)
        if form.is_valid():
            contract = form.save(commit=False)
            contract.save()
            try:
                del request.session['member_id']
            except KeyError:
                pass
            messages.success(request, f'Contrat créé.')
            return redirect('mvp-contract-details', company.id, contract.id, )
    return render(request, 'mvp/views/contract_form.html', {'form': form})


# @ TODO: renommer en conseildetails ?
@login_required
def CreateContract_Conseil(request, cpny_pk=None, client_pk=None):
    form = LicenseForm(request.POST or None,)
    if request.method == "POST":
        print(request.POST)
        if form.is_valid():
            print("VALID")
    return render(request, 'mvp/views/conseil_details.html', {'form': form})


# @ TODO: A Retravailler
@login_required
def join_company(request):
    if request.method == "POST":
        company = Company.objects.filter(pk=int(request.POST['company_id'])).first()
        if company:
            Commercial.objects.create(user=request.user, company=company)
            return redirect('mvp-commercial-workspace')
        else:
            messages.warning(request, f'Wrong company ID')
    return render(request, 'mvp/base/join_company.html')


@login_required
def commercialWorkspace(request):
    return render(request, 'mvp/workspace/bizdev.html')


@login_required
def ceoWorkspace(request):
    return render(request, 'mvp/workspace/bizdev.html', )
    # return render(request, 'mvp/workspace/manager.html')


@login_required
def workspace(request):
    if hasattr(request.user, 'commercial'):
        return redirect('mvp-commercial-workspace')
    elif hasattr(request.user, 'manager'):
        return redirect('mvp-manager-workspace')
    else:
        return redirect('mvp-join-company')


@login_required
def serviceCreation(request):
    form = ConseilForm(request.POST or None, user=request.user)
    # print(request.POST)
    if request.method == "POST" and form.is_valid():
        if hasattr(request.user, 'commercial'):
            # clean_form = form.save(commit=False)
            # clean_form.company = request.user.commercial.company
            # clean_form.commercial = request.user.commercial
            form.save()
            messages.success(request, f'service created!')
            return redirect('mvp-workspace')
        elif hasattr(request.user, 'manager'):
            # clean_form = form.save(commit=False)
            # clean_form.company = request.user.manager.company
            form.save()
            messages.success(request, f'service created!')
            return redirect('mvp-workspace')
    return render(request, 'mvp/service/service_form.html', {'form': form})


@login_required
def licenseCreation(request):
    form = LicenseForm(request.POST or None, user=request.user)
    if request.method == "POST" and form.is_valid():
        if hasattr(request.user, 'commercial'):
            clean_form = form.save(commit=False)
            clean_form.company = request.user.commercial.company
            clean_form.commercial = request.user.commercial
            form.save()
            messages.success(request, f'license created!')
            return redirect('mvp-workspace')
    return render(request, 'mvp/license/license_form.html', {'form': form})
