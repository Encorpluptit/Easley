from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, CompanyRegisterForm, ClientRegisterForm
from .models import Ceo, Commercial
from .controllers import customRegisterUser, customCompanyRegister
from django.contrib.auth import authenticate, login

from django.contrib.auth.models import User


# Create your views here.


def home(request):
    return render(request, 'mvp/home.html')


def about(request):
    return render(request, 'mvp/about.html')


def contact(request):
    return render(request, 'mvp/contact.html')


def register(request):
    form = UserRegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        if customRegisterUser(request, form):
            return redirect('mvp-login')
            # return redirect('mvp-join-company')
        else:
            messages.error(request, f'An Error occured ! Please try again later')
            return redirect(request, 'mvp-home')
    # return render(request, 'mvp/register.html', locals())
    return render(request, 'mvp/register.html', {'form': form})


@login_required
def company_creation(request):
    form = CompanyRegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        ceo, company = customCompanyRegister(request, form)
        messages.success(request, f'Company { company.name } Created, Welcome { ceo } !')
        return redirect('mvp-home')
    return render(request, 'mvp/company_creation.html', {'form': form})


@login_required
def client_creation(request):
    print(request)
    form = ClientRegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        clean_form = form.save(commit=False)
        commercial_var = Commercial.objects.get(user=request.user)
        if commercial_var:
            clean_form.company = commercial_var.company
        form.save()
        return redirect('mvp-home')
    return render(request, 'mvp/company_creation.html', {'form': form})
