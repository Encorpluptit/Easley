from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# Create your forms here.


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    ceo = forms.BooleanField(required=False)
    # conditions = forms.BooleanField()

    class Meta:
        model = User
        # fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'ceo']

