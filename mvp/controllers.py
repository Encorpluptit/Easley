from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import Ceo


def customRegisterUser(request, form):
    user = form.save()
    auth = authenticate(request,
                        username=form.cleaned_data['username'],
                        password=form.cleaned_data['password1'])
    if auth is not None:
        login(request, auth)
        messages.success(request,
                         f'Account Created, Welcome {user.first_name + " " + user.last_name} !'
                         f'Please make a choice.')
        return True
    else:
        return False


def customCompanyRegister(request, form):
    clean_form = form.save(commit=False)
    ceo = Ceo.objects.create(user=request.user)
    ceo.save()
    clean_form.ceo = ceo
    return ceo, form.save()
