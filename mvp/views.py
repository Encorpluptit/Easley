from django.shortcuts import render, redirect
from .forms import UserRegisterForm, CompaniesRegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login

from django.contrib.auth.models import User


# Create your views here.


def home(request):
    return render(request, 'mvp/home.html')


def register(request):
    form = UserRegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        if form.cleaned_data.get('ceo', False):
            auth = authenticate(request, username=form.cleaned_data['username'],
                                password=form.cleaned_data['password1'])
            if auth is not None:
                login(request, auth)
                messages.success(request,
                                 f'Account Created, Welcome {user.first_name + " " + user.last_name} ! '
                                 f'Please create your Company.')

                return redirect('mvp-company-register')
        else:
            messages.success(request,
                             f'Account Created, Welcome {user.first_name + " " + user.last_name} ! Please Login.')
            return redirect('mvp-login')
    # return render(request, 'mvp/register.html', locals())
    return render(request, 'mvp/register.html', {'form': form})


# @TODO: Add CEO CREATION, remove PROFILE refs
def company_creation(request):
    form = CompaniesRegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        # @TODO: Add try except for unique ceo per company
        # @TODO: Add company to ceo Profile
        # raise forms.ValidationError("On ne veut pas entendre parler de pizza !")
        clean_form = form.save(commit=False)
        user_var = request.user
        clean_form.ceo = user_var
        form.save()
        # user_var.profile.type = 3
        # user_var.profile.save()
        # request.user
        return redirect('mvp-home')
    return render(request, 'mvp/company_creation.html', {'form': form})
