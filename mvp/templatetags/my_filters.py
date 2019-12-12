from django import template

register = template.Library()


def currency(money):
    return "{0:2,.2f} €".format(money).replace(",", " ")


register.filter('currency', currency)
