from django import forms
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Company, Commercial, Manager, Client, Service, License, Invoice
from django.core.exceptions import ValidationError


# Create your forms here.


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=150,)
    last_name = forms.CharField(max_length=150,)
    # terms = forms.BooleanField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class': 'form-control'})
            self.fields[key].widget.attrs.update({'placeholder': key})

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

    class Meta:
        model = Company
        exclude = ('ceo',)


class ClientForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(user, 'commercial'):
            self.fields['commercial'].widget = forms.HiddenInput()
        if hasattr(user, 'manager'):
            self.fields['commercial'].queryset = Commercial.objects.filter(company=user.manager.company)
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class': 'form-control'})
            self.fields[key].widget.attrs.update({'placeholder': key})
            self.fields[key].widget.attrs.update({'title': self.fields[key].help_text})
        self.user = user

    class Meta:
        model = Client
        exclude = ('company',)

    def is_valid(self):
        if hasattr(self.user, 'commercial'):
            self.data._mutable = True
            self.data['commercial'] = self.user.commercial.pk
            self.data._mutable = False
        return super().is_valid()


class ServiceForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(user, 'commercial'):
            self.fields['commercial'].widget = forms.HiddenInput()
            self.fields['client'].queryset = Client.objects.filter(commercial=user.commercial)
        if hasattr(user, 'manager'):
            self.fields['commercial'].queryset = Commercial.objects.filter(company=user.manager.company)
            self.fields['client'].queryset = Client.objects.filter(company=user.manager.company)
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class': 'form-control'})
            self.fields[key].widget.attrs.update({'placeholder': key})
            self.fields[key].widget.attrs.update({'title': self.fields[key].help_text})
        self.user = user

    class Meta:
        model = Service
        exclude = ('company',)

    def is_valid(self):
        if hasattr(self.user, 'commercial'):
            self.data._mutable = True
            self.data['commercial'] = self.user.commercial.pk
            self.data._mutable = False
        # elif hasattr(self.user, 'manager'):
        #     client = Client.objects.get(pk=self.data['client'])
        #     if not client or client.commercial.pk != int(self.data['commercial']):
        #         self.add_error('client', "Ce client n'est pas lié à ce commercial")
        #         self.add_error('commercial', "Ce commercial n'est pas lié à ce client")
        #         return False
        return super().is_valid()


class LicenseForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(user, 'commercial'):
            self.fields['commercial'].widget = forms.HiddenInput()
            self.fields['client'].queryset = Client.objects.filter(commercial=user.commercial)
        if hasattr(user, 'manager'):
            self.fields['commercial'].queryset = Commercial.objects.filter(company=user.manager.company)
            self.fields['client'].queryset = Client.objects.filter(company=user.manager.company)
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class': 'form-control'})
            self.fields[key].widget.attrs.update({'placeholder': key})
            self.fields[key].widget.attrs.update({'title': self.fields[key].help_text})
        self.user = user

    class Meta:
        model = License
        exclude = ('company',)

    def is_valid(self):
        if hasattr(self.user, 'commercial'):
            self.data._mutable = True
            self.data['commercial'] = self.user.commercial.pk
            self.data._mutable = False
        # elif hasattr(self.user, 'manager'):
        #     client = Client.objects.get(pk=self.data['client'])
        #     if not client or client.commercial.pk != int(self.data['commercial']):
        #         self.add_error('client', "Ce client n'est pas lié à ce commercial")
        #         self.add_error('commercial', "Ce commercial n'est pas lié à ce client")
        #         return False
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


class InvoiceFrom(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(user, 'commercial'):
            self.fields['commercial'].widget = forms.HiddenInput()
            self.fields['client'].queryset = Client.objects.filter(commercial=user.commercial)
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
        exclude = ('company',)

    def is_valid(self):
        if hasattr(self.user, 'commercial'):
            self.data._mutable = True
            self.data['commercial'] = self.user.commercial.pk
            self.data._mutable = False
        # elif hasattr(self.user, 'manager'):
        #     client = Client.objects.get(pk=self.data['client'])
        #     if not client or client.commercial.pk != int(self.data['commercial']):
        #         self.add_error('client', "Ce client n'est pas lié à ce commercial")
        #         self.add_error('commercial', "Ce commercial n'est pas lié à ce client")
        #         return False
        return super().is_valid()


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

