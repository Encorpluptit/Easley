from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Company, Commercial, Manager, Client, Conseil, License, Invoice, Service, Contract


# Create your forms here.


CONTRACT_FACTURATION = [
    (1, 'Mensuel'),
    (3, 'Trimestriel'),
    (6, 'Semestriel'),
    (12, 'Annuel'),
]


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=150, )
    last_name = forms.CharField(max_length=150, )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
            self.fields[key].widget.attrs.update({'placeholder': key})
            self.fields[key].widget.attrs.update({'title': self.fields[key].help_text})

    class Meta:
        model = Company
        exclude = ('ceo',)


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

    def __init__(self, *args, user=None, client=None, company=None, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(user, 'commercial'):
            self.fields['commercial'].widget = forms.HiddenInput()
            self.fields['commercial'].initial = user.commercial.id
        elif hasattr(user, 'manager'):
            self.fields['commercial'].queryset = company.commercial_set.all()
        if not kwargs.get('instance', None):
            self.fields['commercial'].initial = client.commercial
        self.instance.company = company
        self.instance.client = client
        # self.fields['factu_manager'].queryset = company.manager_set.filter(role=3)
        self.instance.factu_manager = company.manager_set.filter(role=3).first()
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class': 'form-control'})
            self.fields[key].widget.attrs.update({'placeholder': key})
            self.fields[key].widget.attrs.update({'title': self.fields[key].help_text})

    class Meta:
        model = Contract
        exclude = ('client', 'company', 'price', 'validated', 'payed', 'factu_manager')
        widgets = {
        }


class ConseilForm(forms.ModelForm):
    services_excels = forms.FileField(initial=None, required=False, show_hidden_initial=True)

    def __init__(self, *args, user=None, company=None, contract=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.company = company
        self.instance.contract = contract
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class': 'form-control'})
            self.fields[key].widget.attrs.update({'placeholder': key})
            self.fields[key].widget.attrs.update({'title': self.fields[key].help_text})

    class Meta:
        model = Conseil
        exclude = ('contract', 'payed', 'invoice')
        # exclude = ('company', 'contract', 'client', )
        widgets = {
            'start_date': forms.SelectDateWidget,
            'end_date': forms.SelectDateWidget,
        }


class ServiceForm(forms.ModelForm):
    def __init__(self, *args, user=None, company=None, contract=None, conseil=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.conseil = conseil
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class': 'form-control'})
            self.fields[key].widget.attrs.update({'placeholder': key})
            self.fields[key].widget.attrs.update({'title': self.fields[key].help_text})
        self.user = user

    class Meta:
        model = Service
        # exclude = ('company', 'conseil',)
        exclude = ('conseil',)
        widgets = {
            'estimated_date': forms.SelectDateWidget,
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

    class Meta:
        model = License
        exclude = ('contract', 'payed', 'invoice')
        # exclude = ('company', 'contract', 'client', )
        # widgets = {'start_date': forms.SelectDateWidget, 'duration': forms.NumberInput}


class InvoiceFrom(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(user, 'manager'):
            self.fields['commercial'].queryset = Commercial.objects.filter(company=user.manager.company)
            self.fields['client'].queryset = Client.objects.filter(company=user.manager.company)
            # self.fields['client'].queryset = Client.objects.filter(company=user.manager.company)
            # self.fields['client'].queryset = Client.objects.filter(company=user.manager.company)
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class': 'form-control'})
            self.fields[key].widget.attrs.update({'placeholder': key})
            self.fields[key].widget.attrs.update({'title': self.fields[key].help_text})
        self.user = user

    class Meta:
        model = Invoice
        exclude = ('company', '')
        # exclude = ('company', 'contract',)

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
