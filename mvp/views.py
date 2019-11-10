from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

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
    if request.method == "POST":
        # form = UserRegisterForm(request.POST)
        # print("request:\n", request.POST)
        # print(form.cleaned_data.get('username'))
        # print("form:\n", form)
        if form.is_valid():
            # clean_username = form.cleaned_data
            # print(clean_username.get('username'), None)
            t = form.cleaned_data
            print(t['ceo'])
            print("réussi")
            # print(form.ceo)
            clear_ceo = form.cleaned_data.get('ceo', None)
            user = form.save()
            # print(type(user))
            # @ TODO: Login User
            messages.success(request, f'Account Created')
            # @ TODO: redirect à create entreprise si ceo
            if clear_ceo:
                return redirect('company/register')
            else:
                return redirect('mvp-login')
    # else:
        # form = UserRegisterForm()
    return render(request, 'mvp/register.html', locals())
    # return render(request, 'mvp/register.html', {'form': form})
