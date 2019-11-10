from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login

from django.contrib.auth.models import User


# Create your views here.


def home(request):
    return render(request, 'mvp/home.html')


# def login(request):
#     if request.method == "POST":
#         # form = UserLoginForm(request.POST or None)
#         # form = AuthenticationForm(request.POST or None)
#         form = AuthenticationForm(request.POST)
#         try:
#             print("form:\n", form)
#             print("request:\n", request.POST)
#             # print(form.cleaned_data['username'])
#             # print(form.cleaned_data['email'])
#             # print(form.cleaned_data['password'])
#         except Exception as e:
#             print(e)
#         if form.is_valid():
#             # print(form.cleaned_data['username'])
#             return redirect('mvp-home')
#     else:
#         form = AuthenticationForm()
#     return render(request, 'mvp/login.html', {'form': form})


def register(request):
    form = UserRegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        messages.success(request, f'Account Created, Welcome {user.first_name + " " + user.last_name} ! Please Login.')
        # @TODO: redirect à create entreprise si ceo
        if form.cleaned_data.get('ceo', False):
            # @TODO: Login User
            auth = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            if auth is not None:
                login(request, auth)
            return redirect('mvp-company-register', user)
        else:
            return redirect('mvp-login')
    # return render(request, 'mvp/register.html', form)
    # return render(request, 'mvp/register.html', locals())
    return render(request, 'mvp/register.html', {'form': form})
