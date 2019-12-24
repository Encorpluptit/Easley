from dateutil.relativedelta import relativedelta
from datetime import timedelta
from dateutil.utils import today
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum
from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse, Http404

from .pdfCreateInvoice import CreatePDFInvoice
from .controllers import customRegisterUser, CleanInvoicesLate
from .forms import (
    UserRegisterForm,
    CompanyForm,
)
from .models import Manager, Commercial, Service, Invite, InviteChoice, Contract, Company, getInvoiceStorage, Invoice


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
        facturated_date=None,
        date__month__lte=date.month, date__year__lte=date.year
    ).order_by('contract__id', 'price', 'date',).distinct('contract') or None
    # invoices_to_facture = invoices.filter(
    #     facturated_date=None,
    #     date__month__lte=date.month, date__year__lte=date.year
    # ).order_by('contract__id', '-id', 'price', 'date',).distinct('contract') or None
    # invoices_late = invoices.filter(
    #     payed=False,
    #     facturated_date__lte=F('date') + timedelta(days=0)).order_by('price') or None
    invoices_late = invoices.filter(
        payed=False,
        facturated_date__lte=date - timedelta(days=company.facturation_delay)).order_by('price') or None
    # invoices_late = invoices.filter(
    #     payed=False,
    #     facturated_date=F('date') + timedelta(days=company.facturation_delay)).order_by('price') or None
    if invoices_to_facture:
        for inv in invoices_to_facture:
            qs = inv.contract.invoice_set.filter(
                facturated_date=None,
                date__month__lte=date.month,
                date__year__lte=date.year).exclude(pk=inv.pk) or None
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
        instances = formset.save(commit=False)
        for form in instances:
            if (Invite.objects.filter(email=form.email) or None) or (User.objects.filter(email=form.email) or None):
                messages.warning(request, f"Une invitation a déjà été envoyée pour cette adresse email ou\
                un utilsateur avec cette adresse existe déjà.")
                break
            form.save()
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


from django.db.models import F
@login_required
def FactuWorkspace(request):
    context = {
        'section': 'workspace',
    }

    date = today().date()
    factu = request.user.manager
    company = factu.company
    invoices = company.invoice_set.filter(contract__factu_manager=request.user.manager)
    invoices_to_facture = invoices.filter(
        facturated_date=None,
        date__month__lte=date.month, date__year__lte=date.year
    ).order_by('contract__id', 'price', 'date',).distinct('contract') or None
    # invoices_to_facture = invoices.filter(
    #     facturated_date=None,
    #     date__month__lte=date.month, date__year__lte=date.year
    # ).order_by('contract__id', '-id', 'price', 'date',).distinct('contract') or None
    invoices_late = invoices.filter(
        payed=False,
        facturated_date=F('date') + timedelta(days=0)).order_by('price') or None
    # invoices_late = invoices.filter(
    #     payed=False,
    #     facturated_date=F('date') + timedelta(days=company.facturation_delay)).order_by('price') or None
    if invoices_to_facture:
        for inv in invoices_to_facture:
            qs = inv.contract.invoice_set.filter(
                facturated_date=None, date__month__lt=date.month, date__year__lte=date.year) or None
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
    context['invoice_late'] = invoices_late
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
        date__month__lte=date.month, date__year__lte=date.year
    ).order_by('price', 'date',) or None
    amount_late = 0

    if invoices_late:
        amount_late = invoices_late.aggregate(price=Sum('price'))['price'] + invoice.price
        context['late_amount'] = amount_late
    if request.method == "POST":
        # print(request.POST)
        if 'delete_invoice' in request.POST and request.POST['delete_invoice'] != '':
            invoice.delete()
            return redirect('mvp-workspace')
        if 'validate_invoice' in request.POST:
            # print("VALIDATE")
            if invoices_late:
                invoice, invoices_late = CleanInvoicesLate(invoice, invoices_late, amount_late)
            company.refresh_from_db(fields=['invoice_nb', ])
            company.invoice_nb += 1
            company.save()
            invoice.facturated_date = today().date()
            invoice.pdf = CreatePDFInvoice(invoice, company.invoice_nb, date, date + timedelta(days=company.facturation_delay))
            invoice.save()
    context['object'] = invoice
    context['invoices_late'] = invoices_late
    return render(request, 'mvp/views/invoice_facturation.html', context)


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


