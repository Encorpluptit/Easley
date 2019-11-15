from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Company, Client, License, Service


# Create your forms here.


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    # terms = forms.BooleanField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class': 'form-control'})
            self.fields[key].widget.attrs.update({'placeholder': key})

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']


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


class CompanyRegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class': 'form-control'})
            self.fields[key].widget.attrs.update({'placeholder': key})

    class Meta:
        model = Company
        exclude = ('ceo',)


class ClientRegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class': 'form-control'})
            self.fields[key].widget.attrs.update({'placeholder': key})

    class Meta:
        model = Client
        exclude = ('company',)


class ServiceRegisterForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)
    # @ TODO: Add good choices for clients

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class': 'form-control'})
            self.fields[key].widget.attrs.update({'placeholder': key})

    class Meta:
        model = Service
        exclude = ('company', 'commercial',)


class LicenseRegisterForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)
    # @ TODO: Add good choices for clients

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class': 'form-control'})
            self.fields[key].widget.attrs.update({'placeholder': key})

    class Meta:
        model = License
        exclude = ('company', 'commercial',)

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

