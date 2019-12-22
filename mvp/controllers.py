import datetime
from os import path as _path, remove as remove_file

import xlrd
from dateutil.relativedelta import relativedelta
from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.shortcuts import get_object_or_404, redirect
from django.utils.formats import localize as loc

from .models import Manager, Commercial, Contract, Invoice, Service


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
    total_price, unity_price = 0, int(contract.price / invoice_delta)

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
        total_price += unity_price
    if total_price != contract.price:
        invoice.price = contract.price - (total_price - unity_price)
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


def createExcelServices(form):
    if hasattr(form, 'servicelist'):
        conseil = form.instance
        for service in conseil.service_set.all():
            service.delete()
        for data in form.servicelist:
            print(data)
            service = Service(
                conseil=conseil,
                description=data[0],
                estimated_date=data[1],
                senior_day=data[2],
                junior_day=data[3],
            )
            print(service)
            service.save()
        conseil.save(update_fields=['price', ])


def ManageExcelForm(self, data):
    name = "Services_%d_%s" % (self.instance.contract.id, self.user)
    path = "mvp/static/mvp/files/Uploads/%s" % name
    if _path.exists(path):
        remove_file(path)
    f = open(path, 'wb+')
    f.write(data.read())
    f.close()
    excel = xlrd.open_workbook(path)
    if len(excel.sheets()) != 1:
        raise forms.ValidationError("Votre Excel est vide ou contient trop ou de feuilles.")
    try:
        sheet = excel.sheet_by_index(0)
    except:
        raise forms.ValidationError("Votre Excel recontre un problème.")
    prestas_check_list = [
        (1, 'Description', xlrd.sheet.XL_CELL_TEXT),
        (2, 'Date Prévisionelle', xlrd.sheet.XL_CELL_DATE),
        (3, 'Jour-Hommes Senior', xlrd.sheet.XL_CELL_NUMBER),
        (4, 'Jour-Hommes Junior', xlrd.sheet.XL_CELL_NUMBER),
    ]
    self.servicelist = []
    for rowInd in range(1, sheet.nrows):
        values_list = []
        for colInd in range(1, 5):
            cell = sheet.cell(rowInd, colInd)
            if not cell.value and cell.value != 0:
                if colInd > 1 and len(values_list):
                    raise forms.ValidationError(
                        "Votre excel contient une cellule vide dans la section \"%s\""
                        "\nLigne: %d\tColonne: %c\n" % (
                            prestas_check_list[colInd - 1][1], rowInd + 1, chr(64 + colInd + 1)))
                else:
                    continue
            if cell.ctype != prestas_check_list[colInd - 1][2]:
                raise forms.ValidationError(
                    "Votre excel contient une erreur dans la section \"%s\""
                    "\nLigne: %d\tColonne: %c\n" % (
                        prestas_check_list[colInd - 1][1], rowInd + 1, chr(64 + colInd + 1)))
            if colInd == 2:
                date = datetime.datetime(*xlrd.xldate.xldate_as_tuple(cell.value, excel.datemode)).date()
                values_list.append(date)
            else:
                values_list.append(cell.value)
        length = len(values_list)
        if length:
            if length == 4:
                self.servicelist.append(values_list)
            else:
                raise forms.ValidationError(
                    "Votre excel contient une cellule vide dans la section \"Description\""
                    "\nLigne: %d\tColonne: %c\n" % (rowInd + 1, chr(64 + 2)))


def CleanInvoicesLate(invoice, invoices_late, invoice_amount):
    for late in invoices_late:
        late.delete()
    invoices_late = None
    invoice.price = invoice_amount
    return invoice, invoices_late


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


def redirectWorkspaceFail(request, message):
    messages.warning(request, message)
    return redirect('mvp-workspace')
