from django import template

register = template.Library()


def currency(money):
    return '{:20,.2f} €'.format(money)


register.filter('currency', currency)
