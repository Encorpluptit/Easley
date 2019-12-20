from django import template
from django.utils.formats import localize as loc

from mvp.forms import CONTRACT_FACTURATION
from mvp.models import InviteChoice, ServiceStatusChoice

register = template.Library()


@register.filter(name='currency')
def currency(money):
    return "{0:2,.2f} €".format(money).replace(",", " ")


@register.filter(name='Fduration')
def Fduration(facturation):
    for data, s in CONTRACT_FACTURATION:
        if data == facturation:
            return s
    return "N/A"


@register.filter(name='ServiceStatusFilter')
def ServiceStatusFilter(status, actual_date=None):
    if status and not actual_date:
        return "Ne sera jamais effectué"
    elif status and actual_date:
        return "Effectué le: {}".format(loc(actual_date))
    elif not status and not actual_date:
        return "Pas encore effectué"
    else:
        return "N/A"


@register.filter(name='InviteFilter')
def InviteFilter(role):
    for nb, string in InviteChoice:
        if nb == role:
            return string
    return "N/A"
