from dateutil.relativedelta import relativedelta
from datetime import timedelta
from dateutil.utils import today
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum
from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse, Http404, HttpResponse
from mvp.forms import CONTRACT_FACTURATION
import csv

from .pdfCreateInvoice import CreatePDFInvoice
from .controllers import customRegisterUser, CleanInvoicesLate
from .models import License, Service, Contract
from .forms import (
    UserRegisterForm,
    CompanyForm,
)
from .models import Manager, Commercial, Service, Invite, InviteChoice, Invoice, EmailDatabase


# Create your views here.


def home(request):
    if request.method == "POST":
        if EmailDatabase.objects.filter(email=request.POST['email']) or None:
            EmailDatabase.objects.create(email=request.POST['email'])
    return render(request, 'mvp/misc/index.html')


def about(request):
    return render(request, 'mvp/misc/about.html')


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
def viewContractCsv(request):
    if hasattr(request.user, 'commercial') or request.user.manager.role != 1:
        return Http404
    qs = Contract.objects.filter(company=request.user.manager.company)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Détails Contrats.csv"'
    writer = csv.writer(response)
    writer.writerow(['Licence / Conseil', 'Contract', 'Client', 'Date de début', 'Date de fin', 'Periodicité',
                     'Commercial', 'Account manager', 'Montant Total'])
    writer.writerow([])
    for contract in qs:
        for license in contract.license_set.all():
            writer.writerow([license.description, contract.description, contract.client,
                             license.start_date.strftime("%d/%m/%Y"), license.end_date.strftime("%d/%m/%Y"),
                             [x[1] for x in CONTRACT_FACTURATION if x[0] == license.contract.facturation][0],
                             contract.commercial,
                             contract.client.account_manager, str(license.price) + " €"])
        for conseil in contract.conseil_set.all():
            writer.writerow([conseil.description, contract.description, contract.client,
                             conseil.start_date.strftime("%d/%m/%Y"), conseil.end_date.strftime("%d/%m/%Y"),
                             [x[1] for x in CONTRACT_FACTURATION if x[0] == conseil.contract.facturation][0],
                             contract.commercial,
                             contract.client.account_manager, str(conseil.price) + " €"])
    return response


@login_required
def viewInvoiceCsv(request):
    if hasattr(request.user, 'commercial') or request.user.manager.role != 1:
        return Http404
    qs = Invoice.objects.filter(company=request.user.manager.company).order_by('contract__start_date', 'date')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Détails Invoice.csv"'
    writer = csv.writer(response)
    writer.writerow(['N° Facture', 'Contract', 'Client', 'Date de début', 'Date de fin', 'Periodicité',
                     'Date de facturation', 'Date d\'encaissement', 'Commercial', 'Account manager', 'Montant Total'])
    writer.writerow([])
    for invoice in qs:
        writer.writerow([invoice.date.strftime("%Y") + "_" + str(invoice.number) if invoice.facturated_date else "N/A",

                         invoice.contract, invoice.contract.client,
                         invoice.contract.start_date, invoice.contract.end_date,
                         [x[1] for x in CONTRACT_FACTURATION if x[0] == invoice.contract.facturation][0],
                         invoice.facturated_date or "N/A", invoice.payed_date or "N/A",
                         invoice.contract.commercial,
                         invoice.contract.client.account_manager, str(invoice.price) + " €"])
    return response


@login_required
def ManagerWorkspace(request):
    context = {
        'section': 'workspace',
        'to_facture_count': 0,
        'to_facture_amount': 0,
        'late_count': 0,
        'late_amount': 0,
    }

    date = today().date()
    factu = request.user.manager
    company = factu.company
    invoices = company.invoice_set.all()
    invoices_to_facture = invoices.filter(
        facturated_date=None, date__lte=date
    ).order_by('contract__id', 'price', '-date', ).distinct('contract') or None
    invoices_late = invoices.filter(
        payed=False,
        facturated_date__lte=date - timedelta(days=company.facturation_delay)).order_by('price') or None
    if invoices_to_facture:
        for inv in invoices_to_facture:
            qs = inv.contract.invoice_set.filter(
                facturated_date=None,
                date__lte=date).exclude(pk=inv.pk) or None
            if qs:
                inv.late = qs.count()
                inv.late_amount = qs.aggregate(Sum('price'))['price__sum']
        invoices_to_facture.query.distinct_fields = ()
        context['to_facture_count'] = invoices_to_facture.count()
        context['to_facture_amount'] = invoices_to_facture.aggregate(Sum('price'))['price__sum']
    if invoices_late:
        invoices_late.query.distinct_fields = ()
        context['late_count'] = invoices_late.count()
        context['late_amount'] = invoices_late.aggregate(Sum('price'))['price__sum']
    context['invoices_to_facture'] = invoices_to_facture
    context['invoices_late'] = invoices_late
    return render(request, 'mvp/workspace/manager.html', context)


@login_required
def Kpi(request):
    context = {
        'section': 'KPI',
        'mmr': 0,
        'amr': 0,
        'ca_a': 0,
        'ca_m': 0,
    }
    if not hasattr(request.user, 'manager') or request.user.manager.role != 1:
        return Http404
    company = request.user.manager.company
    contracts = company.contract_set.all()
    date = today()
    date_month = date - relativedelta(months=4)
    date_year = date - relativedelta(years=1)
    contracts_year = contracts.filter(start_date__gte=date_year, validated=True)
    contracts_month = contracts.filter(start_date__gte=date_month, validated=True)
    license_year = License.objects.filter(
        contract__company=company,
        start_date__gte=date_year,
        contract__validated=True,
    )
    license_month = License.objects.filter(
        contract__company=company,
        start_date__gte=date_month,
        contract__validated=True,
    )
    service_year = Service.objects.filter(
        conseil__contract__company=company,
        actual_date__gte=date_year,
        conseil__contract__validated=True,
        done__gt=0,
    )
    service_month = Service.objects.filter(
        conseil__contract__company=company,
        actual_date__gte=date_month,
        conseil__contract__validated=True,
        done__gt=0,
    )
    mmr = license_month.aggregate(Sum('price'))['price__sum'] or 0
    mmr += service_month.aggregate(Sum('price'))['price__sum'] or 0
    amr = license_year.aggregate(Sum('price'))['price__sum'] or 0
    amr += service_year.aggregate(Sum('price'))['price__sum'] or 0

    ca_m = contracts_month.aggregate(Sum('price'))['price__sum'] or 0
    ca_y = contracts_year.aggregate(Sum('price'))['price__sum'] or 0

    context['mmr'], context['amr'] = mmr, amr
    context['ca_m'], context['ca_y'] = ca_m, ca_y
    return render(request, 'mvp/workspace/kpi.html', context)


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

    inviteformset = modelformset_factory(Invite, extra=4, exclude=('company', 'role'), )
    formset = inviteformset(request.POST or None, queryset=Invite.objects.none())
    for index, form in enumerate(formset):
        for nb, string in InviteChoice:
            if nb == (index + 1):
                form.instance.role = nb
                form.instance.company = company
                form.fields['email'].widget.attrs.update({'class': 'form-control'})
                break
    if request.method == "POST":
        instances = formset.save(commit=False)
        for form in instances:
            if (Invite.objects.filter(email=form.email) or None) or (User.objects.filter(email=form.email) or None):
                messages.warning(request, f"Une invitation a déjà été envoyée pour cette adresse email ou\
                un utilsateur avec cette adresse existe déjà.")
                break
            form.save()
            invites = company.invite_set.all()
            formset = inviteformset(request.POST or None, queryset=Invite.objects.none())
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
    context['new_clients'] = commercial.client_set.filter(
        created_at__gte=today().date() - relativedelta(months=1)).count()
    return render(request, 'mvp/workspace/bizdev.html', context)


@login_required
def FactuWorkspace(request):
    context = {
        'section': 'workspace',
        'to_facture_count': 0,
        'to_facture_amount': 0,
        'late_count': 0,
        'late_amount': 0,
    }

    date = today().date()
    factu = request.user.manager
    company = factu.company
    invoices = company.invoice_set.filter(contract__factu_manager=request.user.manager)
    invoices_to_facture = invoices.filter(
        facturated_date=None, date__lte=date
    ).order_by('contract__id', 'price', '-date', ).distinct('contract') or None
    invoices_late = invoices.filter(
        payed=False,
        facturated_date__lte=date - timedelta(days=company.facturation_delay)).order_by('price') or None
    if invoices_to_facture:
        for inv in invoices_to_facture:
            qs = inv.contract.invoice_set.filter(
                facturated_date=None,
                date__lte=date).exclude(pk=inv.pk) or None
            if qs:
                inv.late = qs.count()
                inv.late_amount = qs.aggregate(Sum('price'))['price__sum']
        invoices_to_facture.query.distinct_fields = ()
        context['to_facture_count'] = invoices_to_facture.count()
        context['to_facture_amount'] = invoices_to_facture.aggregate(Sum('price'))['price__sum']
    if invoices_late:
        invoices_late.query.distinct_fields = ()
        context['late_count'] = invoices_late.count()
        context['late_amount'] = invoices_late.aggregate(Sum('price'))['price__sum']
    context['invoices_to_facture'] = invoices_to_facture
    context['invoices_late'] = invoices_late
    return render(request, 'mvp/workspace/factu.html', context)


@login_required
def AccountWorkspace(request):
    context = {
        'section': 'workspace',
        'nb_services_to_validate': 0,
        'to_facture_amount': 0,
        'late_count': 0,
        'late_amount': 0,
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
    if services:
        context['nb_services_to_validate'] = services.count()
    context['services'] = services

    date = today().date()
    factu = request.user.manager
    company = factu.company
    invoices = company.invoice_set.filter(contract__client__account_manager=request.user.manager)
    invoices_to_facture = invoices.filter(
        facturated_date=None,
        date__lte=date
    ).order_by('contract__id', 'price', '-date', ).distinct('contract') or None
    invoices_late = invoices.filter(
        payed=False,
        facturated_date__lte=date - timedelta(days=company.facturation_delay)).order_by('price') or None
    if invoices_to_facture:
        for inv in invoices_to_facture:
            qs = inv.contract.invoice_set.filter(
                facturated_date=None,
                date__lte=date).exclude(pk=inv.pk) or None
            if qs:
                inv.late = qs.count()
                inv.late_amount = qs.aggregate(Sum('price'))['price__sum']
        invoices_to_facture.query.distinct_fields = ()
        context['to_facture_amount'] = invoices_to_facture.aggregate(Sum('price'))['price__sum']
    if invoices_late:
        invoices_late.query.distinct_fields = ()
        context['late_count'] = invoices_late.count()
        context['late_amount'] = invoices_late.aggregate(Sum('price'))['price__sum']
    context['invoices_to_facture'] = invoices_to_facture
    context['invoices_late'] = invoices_late
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


@login_required
def doFacturation(request, cpny_pk=None, invoice_pk=None):
    context = {
        'section': 'invoice',
        'content_heading': 'Valider la facture',
    }
    invoice = get_object_or_404(Invoice, pk=invoice_pk)
    company = invoice.contract.company
    date = today().date()
    invoices_late = invoice.contract.invoice_set.exclude(pk=invoice.pk).filter(
        facturated_date=None,
        date__lte=date).order_by('price', '-date', ) or None
    amount_late = 0

    if invoices_late:
        amount_late = invoices_late.aggregate(price=Sum('price'))['price'] + invoice.price
        context['late_amount'] = amount_late
    if request.method == "POST":
        if 'delete_invoice' in request.POST and request.POST['delete_invoice'] != '':
            invoice.delete()
            return redirect('mvp-workspace')
        if 'validate_invoice' in request.POST:
            if invoices_late:
                invoice, invoices_late = CleanInvoicesLate(invoice, invoices_late, amount_late)
            company.refresh_from_db(fields=['invoice_nb', ])
            company.invoice_nb += 1
            company.save()
            invoice.number = company.invoice_nb
            invoice.facturated_date = today().date()
            invoice.pdf = CreatePDFInvoice(invoice, invoice.number, date,
                                           date + timedelta(days=company.facturation_delay))
            invoice.save()
    context['object'] = invoice
    context['invoices_late'] = invoices_late
    return render(request, 'mvp/views/invoice_facturation.html', context)


def doPayedinvoice(request, invoice_pk=None):
    invoice = get_object_or_404(Invoice, pk=invoice_pk)
    invoice.payed_date = today().date()
    invoice.payed = True
    invoice.save()
    return redirect('mvp-workspace')


@login_required
def pdf_download(request, cpny_pk, invoice_pk):
    invoice = get_object_or_404(Invoice, pk=invoice_pk)
    try:
        return FileResponse(open(invoice.pdf.path, 'rb'),
                            content_type='application/pdf',
                            as_attachment=True,
                            filename='Facture.pdf')
    except FileNotFoundError:
        raise Http404()


@login_required
def pdf_view(request, cpny_pk, invoice_pk):
    invoice = get_object_or_404(Invoice, pk=invoice_pk)
    try:
        return FileResponse(open(invoice.pdf.path, 'rb'),
                            content_type='application/pdf',
                            filename='Facture.pdf')
    except FileNotFoundError:
        raise Http404()
