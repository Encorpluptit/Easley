from django import template
from mvp.forms import CONTRACT_FACTURATION
from mvp.models import InviteChoice, ServiceStatusChoice

register = template.Library()


def currency(money):
    return "{0:2,.2f} €".format(money).replace(",", " ")


def Fduration(facturation):
    for data, s in CONTRACT_FACTURATION:
        if data == facturation:
            return s
    return "N/A"


def ServiceStatusFilter(status):
    for nb, string in ServiceStatusChoice:
        if nb == status:
            return string
    return "N/A"


def InviteFilter(role):
    for nb, string in InviteChoice:
        if nb == role:
            return string
    return "N/A"


register.filter('currency', currency)
register.filter('Fduration', Fduration)
register.filter('InviteFilter', InviteFilter)
register.filter('ServiceStatusFilter', ServiceStatusFilter)
