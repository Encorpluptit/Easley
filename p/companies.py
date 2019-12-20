from django.contrib.auth.models import User

from mvp.models import Company
from mvp.models import Manager
from .dict_global import PASSWORD


def CreateCeoManager(user, company, role, dictio, index):
    m = Manager(user=user, company=company, role=role)
    m.save()
    dictio[index] = m
    return m


def CreateCeoUser(first_name, last_name, email, dictio):
    u = User(
        username="%s%s" % (first_name, last_name),
        password=PASSWORD,
        email=email,
        first_name=first_name,
        last_name=last_name,
    )
    u.set_password(PASSWORD)
    u.save()
    dictio[str(u)] = u
    return u


def CreateCompany(user, siret, junior_day, senior_day, name, dictio, index):
    c = Company(
        ceo=user,
        name=name,
        siret=siret,
        junior_day=junior_day,
        senior_day=senior_day,
    )
    c.save()
    dictio[index] = c
    return c


def CreateAllCompanies(DATA):
    datas = [
        ["Enis", "Msyr", "enis@easleyfin.io",
         "00000000000000", 250, 500, "Entreprise d'Enis"],
        ["Eliot", "Barragne", "eliot@easleyfin.io",
         "11111111111111", 125, 250, "Entreprise d'Eliot"],
        ["Damien", "Bernard", "damien.bernard@epitech.eu",
         "22222222222222",  250, 500, "Entreprise de Damien"],
    ]
    i = 1
    for data in datas:
        try:
            ceo_user = CreateCeoUser(data[0], data[1], data[2], DATA['Users'])
            company = CreateCompany(
                ceo_user, data[3], data[4], data[5], data[6], DATA['Companies'], i)
            manager = CreateCeoManager(ceo_user, company, 1, DATA['Managers'], i)
            i += 1
        except Exception as e:
            print("in create all companies:\n", e)
