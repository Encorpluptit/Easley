from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms import modelformset_factory
from dateutil.relativedelta import relativedelta
from dateutil.utils import today
from django.db.models import Sum
from .models import Manager, Commercial, Service, Invite, InviteChoice
from .controllers import customRegisterUser
from .forms import (
    UserRegisterForm,
    CompanyForm,
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
            return redirect('mvp-company-register')
        else:
            return redirect(request, 'mvp-home')
    return render(request, 'mvp/misc/register.html', {'form': form})


@login_required
def companyCreation(request):
    form = CompanyForm(request.POST or None, ceo=request.user)
    if request.method == "POST" and form.is_valid():
        try:
            company = form.save()
            ceo = Manager.objects.create(user=request.user, company=company, role=1)
            ceo.save()
            messages.success(request, f'Company {company.name} Created, Welcome {ceo} !')
            return redirect('mvp-employees')
        except:
            messages.warning(request, f'An Error occurred ! Please try again later')
        return redirect('mvp-workspace')
    return render(request, 'mvp/misc/company_creation.html', {'form': form})


def join_company(request, invite_email):
    invite = get_object_or_404(Invite, email=invite_email)
    form = UserRegisterForm(request.POST or None, email=invite_email)
    if request.method == "POST" and form.is_valid():
        if customRegisterUser(request, form):
            if 1 <= invite.role <= 3:
                manager = Manager.objects.create(user=request.user, company=invite.company, role=invite.role)
            elif invite.role == 4:
                commercial = Commercial.objects.create(user=request.user, company=invite.company)
            else:
                messages.warning(request, f"Une erreur s'est produite !")
                return render(request, 'mvp/misc/register.html', {'form': form})
            invite.delete()
            return redirect('mvp-workspace')
        else:
            return redirect(request, 'mvp-home')
    return render(request, 'mvp/misc/register.html', {'form': form})


@login_required
def ManagerWorkspace(request):
    context = {
        'section': 'workspace',
    }
    return render(request, 'mvp/workspace/manager.html', context)


@login_required
def Employees(request):
    company = request.user.manager.company
    managers = company.manager_set.all()
    invites = company.invite_set.all()
    context = {
        'section': "employees",
        'commercials': company.commercial_set.all() or None,
        'factus': managers.filter(role=3) or None,
        'accounts': managers.filter(role=2) or None,
        'managers': managers.filter(role=1) or None,
    }

    inviteformset = modelformset_factory(Invite, extra=4, exclude=('company', 'role'),)
    formset = inviteformset(request.POST or None, queryset=Invite.objects.none())
    for index, form in enumerate(formset):
        for nb, string in InviteChoice:
            if nb == (index + 1):
                form.instance.role = nb
                form.instance.company = company
                form.fields['email'].widget.attrs.update({'class': 'form-control'})
                break
    if request.method == "POST":
        # print("POST\n", request.POST)
        # print(formset.is_valid())
        instances = formset.save(commit=False)
        # print(instances)
        for form in instances:
            # print('form in instance', form, type(form))
            if (Invite.objects.filter(email=form.email) or None) or (User.objects.filter(email=form.email) or None):
                messages.warning(request, f"Une invitation a déjà été envoyée pour cette adresse email ou\
                un utilsateur avec cette adresse existe déjà.")
                break
            # print('save')
            form.save()
            # formset.full_clean()
            # formset._should_delete_form(form)
            # formset.delete_existing(form)
    context['invites'] = invites
    context['invite_commercial'] = invites.filter(role=4) or None
    context['invite_factus'] = invites.filter(role=3) or None
    context['invite_accounts'] = invites.filter(role=2) or None
    context['invite_managers'] = invites.filter(role=1) or None
    context['formset'] = formset
    return render(request, 'mvp/misc/employees.html', context)


@login_required
def CommercialWorkspace(request):
    context = {
        'section': 'workspace',
        'month_prime': 0,
        'year_prime': 0,
    }
    commercial = request.user.commercial
    contracts = commercial.contract_set.all()
    date = today()
    month_prime = contracts.filter(start_date__month=date.month, validated=True).aggregate(Sum('price'))['price__sum']
    year_prime = contracts.filter(start_date__year=date.year, validated=True).aggregate(Sum('price'))['price__sum']
    if month_prime:
        context['month_prime'] = month_prime / 10
    if year_prime:
        context['year_prime'] = year_prime / 10
    context['unfinished_contracts'] = contracts.filter(validated=False).count()
    context['finished_contracts'] = contracts.filter(validated=True).count()
    context['new_clients'] = commercial.client_set.filter(created_at__gte=today().date() - relativedelta(months=1)).count()
    return render(request, 'mvp/workspace/bizdev.html', context)


@login_required
def FactuWorkspace(request):
    context = {
        'section': 'workspace',
    }

    date = today()
    factu = request.user.manager
    company = factu.company
    invoices = company.invoice_set.all()
    context['invoice_to_facture'] = invoices.filter(
        contract__factu_manager=factu, facturated=False,
        date__month__lte=date.month, date__year__lte=date.year
    ).order_by('contract__id', 'price', 'date',).distinct('contract')
    # invoices = company.invoice_set.order_by('contract__id', 'date').distinct('contract')
    # context['invoice_to_facture'] = invoices.filter(
    #     contract__factu_manager=factu, facturated=False,
    #     date__month__lte=date.month, date__year__lte=date.year)
    context['invoice_late'] = invoices.filter(
        contract__factu_manager=factu, facturated=True, payed=False,
        date__month__lte=date.month, date__year__lte=date.year).order_by('price')
    for inv in context['invoice_to_facture']:
        qs = inv.contract.invoice_set.filter(
            facturated=False, date__month__lt=date.month, date__year__lte=date.year) or None
        # print(inv)
        # print(qs)
        if qs:
            inv.late = qs.count()
    return render(request, 'mvp/workspace/factu.html', context)


@login_required
def AccountWorkspace(request):
    context = {
        'section': 'workspace',
        'nb_services_to_validate': 0,
    }
    manager = request.user.manager
    date = today()
    services = Service.objects.filter(
        conseil__contract__company=manager.company,
        conseil__contract__validated=True,
        conseil__contract__client__account_manager=manager,
        estimated_date__month__lte=date.month,
        estimated_date__year__lte=date.year,
    )
    print(services)
    if services:
        context['nb_services_to_validate'] = services.count()
    context['services'] = services
    return render(request, 'mvp/workspace/account.html', context)


@login_required
def workspace(request):
    user = request.user
    if hasattr(user, 'commercial'):
        return CommercialWorkspace(request)
    elif hasattr(user, 'manager'):
        if user.manager.role == 1:
            return ManagerWorkspace(request)
        elif user.manager.role == 2:
            return AccountWorkspace(request)
        elif user.manager.role == 3:
            return FactuWorkspace(request)
    return redirect('mvp-company-register')












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
