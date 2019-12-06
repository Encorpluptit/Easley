from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from dateutil.relativedelta import relativedelta
from django.db.models import Sum
from .models import Manager, Commercial, Contract, Client, Conseil, Invoice


def customRegisterUser(request, form):
    user = form.save()
    auth = authenticate(request,
                        username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
    if auth is not None:
        login(request, auth)
        messages.success(request, f'Account Created, Welcome %s %s !' % (user.first_name, user.last_name))
        return True
    else:
        messages.warning(request, f'An Error occurred ! Please try again later')
        return False

def CreateAllInvoice(contract, licenses, conseils):
    factu_date = contract.start_date + relativedelta(months=+contract.facturation)
    tmp = contract.start_date + relativedelta(days=-1)
    month = contract.facturation
    while factu_date <= contract.end_date:
        # print(factu_date)
        invoice_licenses = licenses.filter(end_date__lte=factu_date, end_date__gt=tmp).all()
        invoice_conseils = conseils.filter(end_date__lte=factu_date, end_date__gt=tmp).all()
        price = invoice_conseils.aggregate(Sum('price'))['price__sum'] or 0
        price += invoice_licenses.aggregate(Sum('price'))['price__sum'] or 0
        # print(invoice_licenses, invoice_conseils)
        # print(price)
        factu = Invoice(description="facttu mois %d" % month,
                        company=contract.company,
                        contract=contract,
                        price=price,
                        date=factu_date,
                        )
        factu.save()
        for lic in invoice_licenses:
            lic.invoice = factu
            lic.save()
        for conseil in invoice_conseils:
            conseil.invoice = factu
            conseil.save()
        tmp = factu_date
        factu_date += relativedelta(months=+contract.facturation)
        month += contract.facturation
    # print(contract.end_date - contract.start_date)
    # print(int((contract.end_date - contract.start_date).days/30))


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
    kwargs['contract'] = get_object_or_404(Contract, pk=self.kwargs.get(self.pk_url_kwarg))
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
        if manager.company.id == self.kwargs.get('cpny_pk') and manager.company == base_class.objects.get(pk=self.kwargs.get(key_pk)).company:
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
        if manager.company.id == self.kwargs.get('cpny_pk') and manager.company == base_class.objects.get(pk=self.kwargs.get(key_pk)).company:
            if manager.role == 3:
                return False
            return True
    except ObjectDoesNotExist:
        return False


def routeDetailsPermissions(self, key_pk, base_class):
    try:
        manager = Manager.objects.get(user=self.request.user)
        if manager.company.id == self.kwargs.get('cpny_pk') and manager.company == base_class.objects.get(pk=self.kwargs.get(key_pk)).company:
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
