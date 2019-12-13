from django import template
from mvp.forms import CONTRACT_FACTURATION

register = template.Library()

# CONTRACT_FACTURATION = [
#     (1, 'Mensuel'),
#     (3, 'Trimestriel'),
#     (6, 'Semestriel'),
#     (12, 'Annuel'),
# ]


def currency(money):
    return "{0:2,.2f} €".format(money).replace(",", " ")


def Fduration(facturation):
    for data, s in CONTRACT_FACTURATION:
        if data == facturation:
            return s
    return "lol"


register.filter('currency', currency)
register.filter('Fduration', Fduration)
