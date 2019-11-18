from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import Manager, Commercial, Client, Service
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.shortcuts import get_object_or_404


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
        messages.warning(request, f'An Error occurred ! Please try again later')
        return False


def customCompanyRegister(request, form):
    try:
        # clean_form = form.save(commit=False)
        # clean_form.ceo = request.user
        company = form.save()
        ceo = Manager.objects.create(user=request.user, company=company)
        ceo.save()
        messages.success(request, f'Company {company.name} Created, Welcome {ceo} !')
    except ValidationError:
        messages.warning(request, f'An Error occurred ! Please try again later')


def routeDetailsPermissions(self, key_pk, base_class):
    try:
        manager = Manager.objects.get(user=self.request.user)
        print(manager)
        if manager.company.id == self.kwargs.get('cpny_pk') and manager.company == base_class.objects.get(pk=self.kwargs.get(key_pk)).company:
            return True
    except ObjectDoesNotExist:
        base_class = get_object_or_404(base_class, pk=self.kwargs.get(key_pk))
        if base_class.commercial == self.request.user.commercial:
            return True
        else:
            return False
    print("ici")

# @TODO à retravailler
def routeCreatePermissions(self, base_class):
    try:
        if Manager.objects.get(user=self.request.user).company.id == self.kwargs.get('cpny_pk'):
            return True
    except ObjectDoesNotExist:
        base_class = get_object_or_404(base_class, pk=self.kwargs.get(key_pk))
        if base_class.company == self.request.user.commercial:
            return True
        else:
            return False


def routeListPermissions(self, key_pk):
    try:
        if Manager.objects.get(user=self.request.user).company.id == self.kwargs.get('cpny_pk'):
            return True
    except ObjectDoesNotExist:
        commercial = get_object_or_404(Commercial, user=self.request.user)
        if commercial.id == self.kwargs.get(key_pk):
            return True
        else:
            return False
