from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from dateutil.relativedelta import relativedelta
from django.utils.formats import localize as loc

from .models import Manager, Commercial, Contract, Client, Conseil, Invoice


def customRegisterUser(request, form):
    user = form.save()
    auth = authenticate(request,
                        username=form.cleaned_data['username'],
                        password=form.cleaned_data['password1'])
    if auth is not None:
        login(request, auth)
        messages.success(request, f'Account Created, Welcome %s %s !' % (user.first_name, user.last_name))
        return True
    else:
        messages.warning(request, f'An Error occurred ! Please try again later')
        return False


def CreateAllInvoice(contract, licenses, conseils):
    invoice, invoice_date, invoice_next_date = None, contract.start_date, contract.start_date
    invoice_delta = int(contract.duration / contract.facturation)
    if invoice_delta * contract.facturation < contract.duration:
        invoice_delta += 1
    # @TODO: factu par mois ?
    total_price, unity_price = 0, (contract.price / invoice_delta)
    print(invoice_delta)
    print(unity_price)

    while invoice_next_date < contract.end_date:
        invoice_date = invoice_next_date
        invoice_next_date += relativedelta(months=+contract.facturation)
        invoice = Invoice.objects.create(
            description="facture du %s" % loc(invoice_date),
            company=contract.company,
            contract=contract,
            price=unity_price,
            date=invoice_date,
        )
        invoice_licenses = licenses.filter(start_date__lt=invoice_next_date, end_date__gt=invoice_date).all() or None
        invoice_conseils = conseils.filter(start_date__lt=invoice_next_date, end_date__gt=invoice_date).all() or None
        if invoice_licenses:
            for license in invoice_licenses:
                invoice.licenses.add(license)
        if invoice_conseils:
            for conseil in invoice_conseils:
                invoice.conseils.add(conseil)
        print("%s\t%s\n%s" % (invoice, invoice.price, loc(invoice.date)))
        print(invoice.conseils.all(), invoice.licenses.all())
        total_price += unity_price
    if total_price != contract.price:
        invoice.price = contract.price - total_price
        invoice.save()


def customCompanyRegister(request, form):
    try:
        company = form.save()
        ceo = Manager.objects.create(user=request.user, company=company, role=1)
        ceo.save()
        messages.success(request, f'Company {company.name} Created, Welcome {ceo} !')
    except ValidationError:
        messages.warning(request, f'An Error occurred ! Please try again later')


def FillConseilLicenseForm(self, model_view, *args, **kwargs):
    kwargs = super(model_view, self).get_form_kwargs()
    kwargs['user'] = self.request.user
    if hasattr(self.request.user, 'manager'):
        kwargs['company'] = self.request.user.manager.company
    elif hasattr(self.request.user, 'commercial'):
        kwargs['company'] = self.request.user.commercial.company
    kwargs['contract'] = get_object_or_404(Contract, pk=self.kwargs.get('contract_pk'))
    return kwargs


def validateCompanyInFormCreateUpdateView(self, form):
    try:
        if hasattr(self.request.user, 'commercial'):
            form.instance.company = self.request.user.commercial.company
        elif hasattr(self.request.user, 'manager'):
            form.instance.company = self.request.user.manager.company
    except ObjectDoesNotExist:
        return redirectWorkspaceFail(self.request, f"Une erreur est survenue.")
    try:
        self.object = form.save()
    except ValidationError:
        return redirectWorkspaceFail(self.request, f"Une erreur est survenue.")
    else:
        return redirect(self.get_success_url())


def routeCreatePermissions(self, cpny_pk, base_class):
    try:
        manager = Manager.objects.get(user=self.request.user)
        if manager.company.id == cpny_pk:
            if manager.role == 3:
                return False
            return True
    except ObjectDoesNotExist:
        commercial = get_object_or_404(Commercial, user=self.request.user)
        if commercial.company.id == cpny_pk:
            return True
        else:
            return False


def routeUpdatePermissions(self, key_pk, base_class):
    try:
        manager = Manager.objects.get(user=self.request.user)
        if manager.company.id == self.kwargs.get('cpny_pk') and manager.company == base_class.objects.get(
                pk=self.kwargs.get(key_pk)).company:
            if manager.role == 3:
                return False
            return True
    except ObjectDoesNotExist:
        base_class = get_object_or_404(base_class, pk=self.kwargs.get(key_pk))
        if base_class.commercial == self.request.user.commercial:
            return True
        else:
            return False


def routeDeletePermissions(self, key_pk, base_class):
    try:
        manager = Manager.objects.get(user=self.request.user)
        if manager.company.id == self.kwargs.get('cpny_pk') and manager.company == base_class.objects.get(
                pk=self.kwargs.get(key_pk)).company:
            if manager.role == 3:
                return False
            return True
    except ObjectDoesNotExist:
        return False


def routeDetailsPermissions(self, key_pk, base_class):
    try:
        manager = Manager.objects.get(user=self.request.user)
        if manager.company.id == self.kwargs.get('cpny_pk') and manager.company == base_class.objects.get(
                pk=self.kwargs.get(key_pk)).company:
            return True
        else:
            return False
    except ObjectDoesNotExist:
        base_class = get_object_or_404(base_class, pk=self.kwargs.get(key_pk))
        if self.kwargs.get('cpny_pk') != self.request.user.commercial.company.id:
            return False
        elif base_class.commercial == self.request.user.commercial:
            return True
        else:
            return False


def routeListPermissions(self, key_pk):
    try:
        if Manager.objects.get(user=self.request.user).company.id == self.kwargs.get('cpny_pk'):
            return True
    except ObjectDoesNotExist:
        commercial = get_object_or_404(Commercial, user=self.request.user)
        if commercial.id == self.kwargs.get(key_pk):
            return True
        else:
            return False


def routeCreateUpdateInvoicePermissions(self, cpny_pk):
    if hasattr(self.request.user, 'manager'):
        manager = get_object_or_404(Manager, user=self.request.user)
        if manager.company.id != cpny_pk or (manager.role != 1 and manager.role != 3):
            return False
        return True
    else:
        return False


def routeListDetailsInvoicePermissions(self, cpny_pk):
    if hasattr(self.request.user, 'manager'):
        if self.kwargs.get('cpny_pk') != self.request.user.manager.company.id:
            return False
        return True
    return False


def redirectWorkspaceFail(request, message):
    messages.warning(request, message)
    return redirect('mvp-workspace')
