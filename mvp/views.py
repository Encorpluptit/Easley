from django.shortcuts import render, redirect
from .forms import UserRegisterForm, CompanyRegisterForm, ClientRegisterForm
from .models import Ceo, Commercial
from django.contrib import messages
from django.contrib.auth import authenticate, login

from django.contrib.auth.models import User


# Create your views here.


def home(request):
    # @TODO: rajouter context pour boutton vers espace perso (ceo ou commercial ou rejoindre)
    return render(request, 'mvp/home.html')


def about(request):
    return render(request, 'mvp/about.html')


def contact(request):
    return render(request, 'mvp/contact.html')


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
            # @ TODO : remove CEO management and login redirect to choice page
            messages.success(request,
                             f'Account Created, Welcome {user.first_name + " " + user.last_name} ! Please Login.')
            return redirect('mvp-login')
    # return render(request, 'mvp/register.html', locals())
    return render(request, 'mvp/register.html', {'form': form})


# @TODO: Add CEO CREATION, remove PROFILE refs
def company_creation(request):
    form = CompanyRegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        # @TODO: Add try except for unique ceo per company
        # raise forms.ValidationError("On ne veut pas entendre parler de pizza !")
        clean_form = form.save(commit=False)
        ceo = Ceo.objects.create(user=request.user)
        ceo.save()
        clean_form.ceo = ceo
        # clean_form.ceo = request.user
        company = form.save()
        messages.success(request, f'Company { company.name } Created, Welcome { ceo } !')
        return redirect('mvp-home')
    return render(request, 'mvp/company_creation.html', {'form': form})


def client_creation(request):
    print(request)
    form = ClientRegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        # @TODO différencier CEO et Commercial si liés aux clients ?
        # raise forms.ValidationError("On ne veut pas entendre parler de pizza !")
        clean_form = form.save(commit=False)
        commercial_var = Commercial.objects.get(user=request.user)
        print(commercial_var.company)
        if commercial_var:
            clean_form.company = commercial_var.company
        form.save()
        return redirect('mvp-home')
    return render(request, 'mvp/company_creation.html', {'form': form})
