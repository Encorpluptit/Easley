from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Companies


# Create your forms here.


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    ceo = forms.BooleanField(required=False)
    # terms = forms.BooleanField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2', 'ceo']
        # fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2', 'ceo', 'terms']


class CompaniesRegisterForm(forms.ModelForm):
    class Meta:
        model = Companies
        fields = '__all__'