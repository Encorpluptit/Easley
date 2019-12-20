from dateutil.relativedelta import relativedelta
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.formats import localize

from .controllers import ManageExcelForm
from .models import (
    Company,
    Commercial,
    Client,
    Conseil,
    License,
    Invoice,
    Service,
    Contract,
    Invite,
)

# Create your forms here.


CONTRACT_FACTURATION = [
    (1, 'Mensuelle'),
    (3, 'Trimestrielle'),
    (6, 'Semestrielle'),
    (12, 'Annuelle'),
]


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=150, )
    last_name = forms.CharField(max_length=150, )

    def __init__(self, *args, email=None, **kwargs):
        super().__init__(*args, **kwargs)
        if email:
            self.fields['email'].widget = forms.HiddenInput()
            self.fields['email'].initial = email
            print(email)
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class': 'form-control'})
            self.fields[key].widget.attrs.update({'placeholder': key})
            self.fields[key].widget.attrs.update({'title': self.fields[key].help_text})

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']


class CompanyForm(forms.ModelForm):
    def __init__(self, *args, ceo=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.ceo = ceo
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class': 'form-control'})
            self.fields[key].widget.attrs.update({'placeholder': self.fields[key].help_text})
            self.fields[key].widget.attrs.update({'title': self.fields[key].help_text})

    class Meta:
        model = Company
        exclude = ('ceo', 'invoice_nb')

    def clean_siret(self):
        data = self.cleaned_data['siret']
        print(type(data))
        print(len(data))
        if len(data) != 14:
            raise forms.ValidationError("Le numéro SIRET doit comporter 14 chiffres.")
        elif not data.isdigit():
            raise forms.ValidationError("Le numéro SIRET ne doit comporter que des chiffres.")
        return data


class ClientForm(forms.ModelForm):
    def __init__(self, *args, user=None, company=None, manager=None, **kwargs):
        super().__init__(*args, **kwargs)
        if not manager:
            self.fields['commercial'].widget = forms.HiddenInput()
            self.fields['commercial'].initial = user.commercial.id
        else:
            self.fields['commercial'].queryset = company.commercial_set.all()
        if not kwargs.get('instance', None):
            self.fields['account_manager'].initial = company.manager_set.filter(role=2).first()
        self.instance.company = company
        self.fields['account_manager'].queryset = company.manager_set.filter(role=2)
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class': 'form-control'})
            self.fields[key].widget.attrs.update({'placeholder': key})
            self.fields[key].widget.attrs.update({'title': self.fields[key].help_text})

    class Meta:
        model = Client
        exclude = ('company',)


class ContractForm(forms.ModelForm):
    facturation = forms.ChoiceField(choices=CONTRACT_FACTURATION)

    def __init__(self, *args, user=None, client=None, company=None, contract=None, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(user, 'commercial'):
            self.fields['commercial'].widget = forms.HiddenInput()
            self.fields['commercial'].initial = user.commercial.id
        elif hasattr(user, 'manager'):
            self.fields['commercial'].queryset = company.commercial_set.all()
        if not kwargs.get('instance', None):
            self.fields['commercial'].initial = client.commercial.id
        self.instance.company = company
        self.instance.client = client
        self.instance.factu_manager = company.manager_set.filter(role=3).first()
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class': 'form-control'})
            self.fields[key].widget.attrs.update({'placeholder': key})
            self.fields[key].widget.attrs.update({'title': self.fields[key].help_text})
        self.fields['start_date'].widget.attrs.update({'data-toggle': 'datepicker'})

    class Meta:
        model = Contract
        exclude = ('client', 'company', 'price', 'validated', 'payed', 'factu_manager', 'end_date')
        widgets = {
        }


class ConseilForm(forms.ModelForm):
    prestas = forms.FileField(
        initial=None,
        required=False,
    )

    def __init__(self, *args, user=None, company=None, contract=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.company = company
        self.instance.contract = contract
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class': 'form-control'})
            self.fields[key].widget.attrs.update({'placeholder': key})
            self.fields[key].widget.attrs.update({'title': self.fields[key].help_text})
        self.fields['start_date'].widget.attrs.update({'data-toggle': 'datepicker'})
        self.fields['prestas'].widget.attrs.update({'style': 'height: auto'})
        self.user = user

    class Meta:
        model = Conseil
        exclude = ('contract', 'payed', 'end_date')

    def clean_prestas(self):
        data = self.cleaned_data['prestas']
        if not data:
            return data
        ManageExcelForm(self, data)
        return data


class ServiceForm(forms.ModelForm):
    def __init__(self, *args, user=None, company=None, contract=None, conseil=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.conseil = conseil
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class': 'form-control'})
            self.fields[key].widget.attrs.update({'placeholder': key})
            self.fields[key].widget.attrs.update({'title': self.fields[key].help_text})
        self.fields['estimated_date'].widget.attrs.update({'data-toggle': 'datepicker'})
        self.user = user

    class Meta:
        model = Service
        exclude = ('conseil', 'payed', 'done', 'actual_date', 'price')
        widgets = {
            'actual_date': forms.SelectDateWidget,
        }


class LicenseForm(forms.ModelForm):
    def __init__(self, *args, user=None, company=None, contract=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.company = company
        self.instance.contract = contract
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class': 'form-control'})
            self.fields[key].widget.attrs.update({'placeholder': key})
            self.fields[key].widget.attrs.update({'title': self.fields[key].help_text})
        self.fields['start_date'].widget.attrs.update({'data-toggle': 'datepicker'})

    class Meta:
        model = License
        exclude = ('contract', 'payed', 'end_date')

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = start_date + relativedelta(months=+cleaned_data['duration'])
        if start_date < self.instance.contract.start_date:
            self.add_error('start_date', "la date de début est inférieure à la date de début du contrat")
        elif end_date > self.instance.contract.end_date:
            self.add_error('duration', 'la date de fin est après à la date de fin du contrat')
            self.add_error('duration', 'License: %s' % localize(end_date))
            self.add_error('duration', 'Contrat: %s' % localize(self.instance.contract.end_date))


class InvoiceFrom(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(user, 'manager'):
            self.fields['commercial'].queryset = Commercial.objects.filter(company=user.manager.company)
            self.fields['client'].queryset = Client.objects.filter(company=user.manager.company)
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class': 'form-control'})
            self.fields[key].widget.attrs.update({'placeholder': key})
            self.fields[key].widget.attrs.update({'title': self.fields[key].help_text})
        self.user = user

    class Meta:
        model = Invoice
        exclude = ('company', '')

    def is_valid(self):
        if hasattr(self.user, 'commercial'):
            self.data._mutable = True
            self.data['commercial'] = self.user.commercial.pk
            self.data._mutable = False
        return super().is_valid()


class UserUpdateForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class': 'form-control'})
            self.fields[key].widget.attrs.update({'placeholder': key})
            self.fields[key].widget.attrs.update({'title': self.fields[key].help_text})

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']


class InviteForm(forms.ModelForm):
    def __init__(self, *args, user=None, role=4, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.company = user.manager.company
        self.instance.role = role
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class': 'form-control'})
            self.fields[key].widget.attrs.update({'placeholder': key})
            self.fields[key].widget.attrs.update({'title': self.fields[key].help_text})
        self.user = user

    class Meta:
        model = Invite
        exclude = ('company', 'role')

# class ClientForm(forms.ModelForm):
#     def __init__(self, *args, user=None, company=None, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.instance.company = company
#         if hasattr(user, 'commercial'):
#             self.fields['commercial'].widget = forms.HiddenInput()
#             self.fields['account_manager'].queryset = Manager.objects.filter(company=user.commercial.company, role=2)
#         if hasattr(user, 'manager'):
#             self.fields['commercial'].queryset = Commercial.objects.filter(company=user.manager.company)
#             self.fields['account_manager'].queryset = Manager.objects.filter(company=user.manager.company, role=2)
#         for key in self.fields:
#             self.fields[key].widget.attrs.update({'class': 'form-control'})
#             self.fields[key].widget.attrs.update({'placeholder': key})
#             self.fields[key].widget.attrs.update({'title': self.fields[key].help_text})
#         self.user = user
#
#     class Meta:
#         model = Client
#         exclude = ('company',)
#
#     def is_valid(self):
#         if hasattr(self.user, 'commercial'):
#             self.data._mutable = True
#             self.data['commercial'] = self.user.commercial.pk
#             self.data._mutable = False
#         return super().is_valid()


# from django.core.validators import validate_email
# class Exemple(forms.BaseModelForm):
#     email = forms.EmailField(validators=[validate_email])
#     first_name = forms.CharField(max_length=150, widget=forms.CharField.widget(attrs={'placeholder': 'first_name'}))
#     required_css_class = 'form-control'
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # self.fields['name'].widget.attrs.update({'placeholder': "Nom de l'entreprise"})
#         for key in self.fields:
#             self.fields[key].widget.attrs.update({'class': 'form-control'})
#             self.fields[key].widget.attrs.update({'placeholder': key})
#
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']
#         exclude = ('first_name',)
#         fields = '__all__'
#         success_url = reverse_lazy('authors')
#         initial = {'date_of_death': '12/10/2016', }
