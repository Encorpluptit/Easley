from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Company, Commercial, Manager, Client, Service, License
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
            # self.fields['commercial'].initial = user.commercial
        if hasattr(user, 'manager'):
            self.fields['commercial'].queryset = Commercial.objects.filter(company=user.manager.company)
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class': 'form-control'})
            self.fields[key].widget.attrs.update({'placeholder': key})

    class Meta:
        model = Client
        exclude = ('company',)

    def save(self, commit=True, user=None):
        if hasattr(user, 'commercial'):
            self.data._mutable = True
            self.data['commercial'] = user.commercial.pk
            self.data._mutable = False
        elif not hasattr(user, 'manager'):
            raise ValidationError
        return super().save(commit=commit)

    def is_valid(self):
        return True
        # return super().is_valid()


class ServiceForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)

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

    class Meta:
        model = Service
        exclude = ('company',)


class LicenseForm(forms.ModelForm):
    # @ TODO: peut-être changer le widget dans init avec
    # widget = forms.Texarea(Et opts comme max_lenght=300 ????????)
    description = forms.CharField(widget=forms.Textarea)

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

    class Meta:
        model = License
        exclude = ('company',)


class UserUpdateForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class': 'form-control'})
            self.fields[key].widget.attrs.update({'placeholder': key})

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']




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

