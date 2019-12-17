from dateutil.utils import today
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import UpdateView
from mvp.controllers import CreateAllInvoice, redirectWorkspaceFail
from mvp.forms import ClientForm, ContractForm
from mvp.modelviews import PERMISSION_DENIED
from mvp.models import Client, Company, Contract


# @ TODO: Faire permissions
@login_required
def CreateContractClient(request, **kwargs):
    context = {
        'page': 'contract_client',
        'post': False,
        'section': 'contract',
        'create_contract': True
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
    context = {}
    client = get_object_or_404(Client, pk=client_pk)
    company = get_object_or_404(Company, pk=cpny_pk)
    form = ContractForm(request.POST or None, user=request.user, client=client, company=company)
    if request.method == "POST":
        if form.is_valid():
            contract = form.save()
            messages.success(request, f'Contrat créé.')
            return redirect('mvp-contract-details', company.id, contract.id, )
    context['form'] = form
    return render(request, 'mvp/views/contract_form.html', context)


class ContractUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Contract
    form_class = ContractForm
    template_name = 'mvp/views/contract_form.html'
    object = None
    pk_url_kwarg = 'contract_pk'
    extra_context = {"update_contract": True, "button": "Modifier le contrat",
                     "page_title": "Easley - Update Contract", "page_heading": "Modifier des contrats",
                     "section": "contract", "content_heading": "Modifier le contrat"}
    permission_denied_message = PERMISSION_DENIED
    success_message = f'Contrat Modifié'

    def test_func(self):
        # @ TODO: Faire permissions.
        return True

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return self.object.get_absolute_url(self.object.company.id)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ContractUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['client'] = kwargs['instance'].client
        kwargs['company'] = kwargs['instance'].company
        return kwargs

    def handle_no_permission(self):
        return redirectWorkspaceFail(self.request, self.permission_denied_message)


# @ TODO: Faire permissions
@login_required
def ContractDetails(request, cpny_pk=None, contract_pk=None, conseil_pk=None):
    context = {
        "page_title": "Easley - Contrat Details", "page_heading": "Gestion des Contrats",
        "section": "contract", "content_heading": "Détail Contrat",
    }
    contract = get_object_or_404(Contract, pk=contract_pk)
    conseils = contract.conseil_set.all().order_by('start_date', '-price') or None
    licenses = contract.license_set.all().order_by('start_date', '-price') or None

    context['object'] = contract
    context['licenses'] = licenses
    context['conseils'] = conseils
    context['invoices'] = contract.invoice_set.all()
    context['progression'] = 0
    date_now = today().date()
    if contract.start_date <= date_now:
        try:
            context['progression'] = int((date_now - contract.start_date) / (contract.end_date - contract.start_date) * 100)
        except ZeroDivisionError:
            pass
    if request.method == "POST" and ('delete_contract' in request.POST):
        contract.delete()
        return redirect('mvp-contract-list', cpny_pk=contract.company.id)
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


# @ TODO: Faire permissions
@login_required
def ContractListView(request, cpny_pk=None):
    context = {'validated_contracts': None, 'section': 'contract', 'list_contract': True}
    if hasattr(request.user, 'commercial'):
        contracts = request.user.commercial.contract_set.all()
        context['validated_contracts'] = contracts.filter(validated=True).order_by('start_date', '-price')
        context['not_validated_contracts'] = contracts.filter(validated=False).order_by('start_date', '-price')
    elif hasattr(request.user, 'manager'):
        contracts = request.user.manager.company.contract_set.all()
        context['validated_contracts'] = contracts.filter(validated=True).order_by('start_date', '-price')
        context['not_validated_contracts'] = contracts.filter(validated=False).order_by('start_date', '-price')
    return render(request, 'mvp/views/contract_list.html', context)
