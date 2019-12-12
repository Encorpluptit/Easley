from mvp.models import Manager
from .dict_global import PASSWORD
from django.contrib.auth.models import User

def CreateOthersManager(company, descr, role, dictio_user, dictio_manager, dictio_index):
    u = User(
        username= "%s_%s" % (descr, company.ceo.first_name),
        password=PASSWORD,
        email="%s_%s@Manager.fr" % (descr, company.ceo.first_name),
        first_name=descr,
        last_name=company.ceo.first_name,
    )
    u.set_password(PASSWORD)
    u.save()
    dictio_user[str(u)] = u
    m = Manager(user=u, company=company, role=role)
    m.save()
    dictio_manager[dictio_index] = m
    return m, dictio_index + 1


def create_managers(AccountData, FactuData, company, dictio_index, DATA):
    for account in AccountData:
        m, dictio_index = CreateOthersManager(
            company=company,
            descr=account['descr'],
            role=account['role'],
            dictio_user=DATA['Users'],
            dictio_manager=DATA['Managers'],
            dictio_index=dictio_index,
        )
    for factu in FactuData:
        m, dictio_index = CreateOthersManager(
            company=company,
            descr=factu['descr'],
            role=factu['role'],
            dictio_user=DATA['Users'],
            dictio_manager=DATA['Managers'],
            dictio_index=dictio_index,
        )
    return dictio_index


def get_data(DATA):
    Enis = {
        'Company': DATA['Companies'][1],
        'AccountManagers': [
            {
                'descr' : "Account",
                'role': 2,}
        ],
        'FactuManager': [
            {
                'descr' : "Factu",
                'role': 3,},
        ],
    }
    Eliot = {
        'Company': DATA['Companies'][2],
        'AccountManagers': [
            {
                'descr' : "Account",
                'role': 2,}
        ],
        'FactuManager': [
            {
                'descr' : "Factu",
                'role': 3,},
        ],
    }
    Damien = {
        'Company': DATA['Companies'][3],
        'AccountManagers': [
            {
                'descr' : "Account",
                'role': 2,}
        ],
        'FactuManager': [
            {
                'descr' : "Factu",
                'role': 3,},
        ],
    }
    return [Enis, Eliot, Damien]


def CreateAllManagers(DATA):
    dictio_index = 4
    managers_datas = get_data(DATA)


    for manager in managers_datas:
        try:
            dictio_index = create_managers(
                AccountData=manager['AccountManagers'],
                FactuData=manager['FactuManager'],
                company=manager['Company'],
                dictio_index=dictio_index, DATA=DATA)
        except Exception as e:
            print("In Create All Managers\n", e)
