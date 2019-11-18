from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Company, Commercial, Manager, Client, Service, License
from .controllers import customRegisterUser, customCompanyRegister
from .forms import (
    UserRegisterForm,
    CompanyForm,
    ClientForm,
    UserUpdateForm,
    ServiceForm,
    LicenseForm,
)
from django.urls import reverse


# Create your views here.


def home(request):
    return render(request, 'mvp/base/home.html')


def about(request):
    return render(request, 'mvp/base/about.html')


def contact(request):
    return render(request, 'mvp/base/contact.html')


def register(request):
    form = UserRegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        if customRegisterUser(request, form):
            return redirect('mvp-join-company')
        else:
            return redirect(request, 'mvp-home')
    return render(request, 'mvp/login_register/register.html', {'form': form})


@login_required
def companyCreation(request):
    form = CompanyForm(request.POST or None, ceo=request.user)
    if request.method == "POST" and form.is_valid():
        customCompanyRegister(request, form)
        return redirect('mvp-home')
    return render(request, 'mvp/forms/company_form.html', {'form': form})


@login_required
def clientCreation(request):
    form = ClientForm(request.POST or None, user=request.user)
    if request.method == "POST":
        if hasattr(request.user, 'commercial'):
            form.data._mutable = True
            form.data['commercial'] = request.user.commercial.pk
        if form.is_valid():
            clean_form = form.save(commit=False)
            clean_form.company = clean_form.commercial.company
            messages.success(request, f'client %s created!' % clean_form.name)
            clean_form = form.save()
            return redirect(clean_form.get_absolute_url(clean_form.company.id))
    return render(request, 'mvp/forms/client_form.html', {'form': form})


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
    return render(request, 'mvp/commercial/commercial_workspace.html')


@login_required
def ceoWorkspace(request):
    return render(request, 'mvp/manager/manager_workspace.html')


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
    form = ServiceForm(request.POST or None, user=request.user)
    # print(form.fields['client'])
    # form.fields['client'] = choice = forms.ChoiceField(choices=[
    # (choice.pk, choice) for choice in Commercial.objects.filter(request.user.commercial.company)])
    if request.method == "POST" and form.is_valid():
        if hasattr(request.user, 'commercial'):
            clean_form = form.save(commit=False)
            clean_form.company = request.user.commercial.company
            clean_form.commercial = request.user.commercial
            form.save()
            messages.success(request, f'service created!')
            return redirect('mvp-workspace')
    return render(request, 'mvp/forms/service_form.html', {'form': form})


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
    return render(request, 'mvp/forms/license_form.html', {'form': form})
