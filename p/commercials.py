from mvp.models import Commercial
from .dict_global import PASSWORD
from django.contrib.auth.models import User


def get_data(DATA):
    Enis = {
        'Company': DATA['Companies'][1],
        'Commercials': [
            {
                'first_name': "Fredy Mercury",
                'last_name': "(commercial_1)",
            },
            {
                'first_name': "Nickel Back",
                'last_name': "(commercial_2)",
            },
            {
                'first_name': "ZZ Top",
                'last_name': "(commercial_3)",
            },
        ],
    }

    Eliot = {
        'Company': DATA['Companies'][2],
        'Commercials': [
            {
                'first_name': "Neville Longbottom",
                'last_name': "(commercial_1)",
            },
            {
                'first_name': "Luna Lovegood",
                'last_name': "(commercial_2)",
            },
            {
                'first_name': "Dobby",
                'last_name': "(commercial_3)",
            },
        ],
    }

    Damien = {
        'Company': DATA['Companies'][3],
        'Commercials': [
            {
                'first_name': "Com 1",
                'last_name': "(commercial_1)",
            },
            {
                'first_name': "Com 2",
                'last_name': "(commercial_2)",
            },
            {
                'first_name': "Com 3",
                'last_name': "(commercial_3)",
            },
        ],
    }
    return [Enis, Eliot, Damien]


def CreateCommercial(company, first_name, last_name, index, dictio_user, dictio_commercial, commercial_index):
    u = User(
        username= "Commercial_%s_%d" % (company.ceo.first_name, index),
        password=PASSWORD,
        email="Commercial_%s_%d@Commercial.fr" % (company.ceo.first_name, index),
        first_name=first_name,
        last_name=last_name
    )
    u.set_password(PASSWORD)
    u.save()
    dictio_user[str(u)] = u
    c = Commercial(user=u, company=company)
    c.save()
    dictio_commercial[commercial_index] = c
    return commercial_index + 1, index + 1


def CreateCompanyCommercials(CompanyData, commercial_index, DATA):
    index = 1
    for commercial in CompanyData['Commercials']:
        commercial_index, index = CreateCommercial(
            company=CompanyData['Company'],
            first_name=commercial['first_name'],
            last_name=commercial['last_name'],
            index=index,
            dictio_user=DATA['Users'],
            dictio_commercial=DATA['Commercials'],
            commercial_index=commercial_index,
        )
    return commercial_index


def CreateAllCommercials(DATA):
    commercial_index = 1
    AllDatas = get_data(DATA)

    for CompanyData in AllDatas:
        try:
            commercial_index = CreateCompanyCommercials(
                CompanyData, commercial_index, DATA)
        except Exception as e:
            print("in Create All Commercial\n", e)
