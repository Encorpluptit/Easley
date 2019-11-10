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
        messages.success(request, f'Account Created, Welcome {user.first_name + " " + user.last_name} ! Please Login.')
        # @TODO: redirect à create entreprise si ceo
        if form.cleaned_data.get('ceo', False):
            # @TODO: Login User
            auth = authenticate(request, username=form.cleaned_data['username'],
                                password=form.cleaned_data['password1'])
            if auth is not None:
                login(request, auth)
            return redirect('mvp-company-register')
        else:
            return redirect('mvp-login')
    # return render(request, 'mvp/register.html', locals())
    return render(request, 'mvp/register.html', {'form': form})


def company_creation(request):
    form = CompaniesRegisterForm(request.POST or None, instance=request.user)
    form.ceo = request.user
    u = request.user
    print(form)
    print(form.ceo)
    if request.method == "POST":
        print("Post réussi", request.POST)
        if form.is_valid():
            print("VALID")
    return render(request, 'mvp/company_creation.html', {'form': form})
