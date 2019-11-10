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
    # required_css_class = 'form-control'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Companies
        exclude = ('ceo',)
        # fields = '__all__'
