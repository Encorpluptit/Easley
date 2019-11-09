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
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        # print("request:\n", request.POST)
        # print(form.cleaned_data.get('username'))
        # print("form:\n", form)
        # @ TODO: faire l'appael du fonction create_user juste après ce if
        if form.is_valid():
            # clean_username = form.cleaned_data
            # print(clean_username.get('username'), None)
            t = form.cleaned_data
            print(t['ceo'])
            print("réussi")
            # print(form.ceo)
            clear_ceo = form.cleaned_data.get('ceo', None)
            form.save()
            # @ TODO: redirect à create entreprise si ceo
            # if clear_ceo:
            #     redirect(create_entrepise)
            # else:
            #     redirect()
            clean_username = form.cleaned_data.get('username', None)
            clear_email = form.cleaned_data.get('email', None)
            if clean_username is not None and clear_email is not None:
                # print(clean_username)
                # print(clear_email)
                # TO DO: match username et adresse et mail
                u = User.objects.filter(username=clean_username, email=clear_email).first()
                # print(u.username, u.email)
        # del form.['ceo']
        # if form.is_valid():
        #     form.save()

    else:
        form = UserRegisterForm()
    # print("form:\n", form)
    return render(request, 'mvp/register.html', {'form': form})
