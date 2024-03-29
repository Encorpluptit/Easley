from datetime import date

from dateutil.relativedelta import relativedelta

from mvp.models import Contract, License, Conseil, Service


def GetDate():
    return date.today()


def GetClient_1Data(nb_contract=1, lic=False, cons=False):
    if nb_contract == 1:
        if lic:
            return [
                {
                    'description': "License_1_Contrat_1",
                    'start_date_offset': {
                        'months': 0,
                        'weeks': 0,
                        'days': 0, },
                    'duration': 6,
                    'price': 10000,
                    'payed': False},
                {
                    'description': "License_2_Contrat_1",
                    'start_date_offset': {
                        'months': 3,
                        'weeks': 0,
                        'days': 0, },
                    'duration': 9,
                    'price': 20000,
                    'payed': False},
            ]
        elif cons:
            return [
                {
                    'description': "Conseil_1_Contrat_1",
                    'start_date_offset': {
                        'months': 0,
                        'weeks': 0,
                        'days': 0, },
                    'duration': 2,
                    'price': 5000,
                    'payed': False,
                    'Services': [
                        {
                            'descr': "début service",
                            'price': 2000,
                            'estimated_date_offset': {
                                'months': 0,
                                'weeks': 0,
                                'days': 0, },
                            'junior_day': 1,
                            'senior_day': 1,
                            'payed': False,
                            'done': 0},
                        {
                            'descr': "mileu service",
                            'price': 2000,
                            'estimated_date_offset': {
                                'months': 0,
                                'weeks': 2,
                                'days': 0, },
                            'junior_day': 2,
                            'senior_day': 2,
                            'payed': False,
                            'done': 0},
                        {
                            'descr': "fin service",
                            'price': 1000,
                            'estimated_date_offset': {
                                'months': 1,
                                'weeks': 2,
                                'days': 0, },
                            'junior_day': 3,
                            'senior_day': 3,
                            'payed': False,
                            'done': 0},
                    ]},

                {
                    'description': "Conseil_2_Contrat_1",
                    'start_date_offset': {
                        'months': 10,
                        'weeks': 0,
                        'days': 0, },
                    'duration': 2,
                    'price': 5000,
                    'payed': False,
                    'Services': [
                        {
                            'descr': "début service",
                            'price': 2000,
                            'estimated_date_offset': {
                                'months': 0,
                                'weeks': 0,
                                'days': 0, },
                            'junior_day': 3,
                            'senior_day': 3,
                            'payed': False,
                            'done': 0},
                        {
                            'descr': "mileu service",
                            'price': 2000,
                            'estimated_date_offset': {
                                'months': 0,
                                'weeks': 2,
                                'days': 0, },
                            'junior_day': 2,
                            'senior_day': 2,
                            'payed': False,
                            'done': 0},
                        {
                            'descr': "fin service",
                            'price': 1000,
                            'estimated_date_offset': {
                                'months': 1,
                                'weeks': 2,
                                'days': 0, },
                            'junior_day': 1,
                            'senior_day': 1,
                            'payed': False,
                            'done': 0},
                    ]},

                {
                    'description': "Conseil_3_Contrat_1",
                    'start_date_offset': {
                        'months': 6,
                        'weeks': 0,
                        'days': 0, },
                    'duration': 2,
                    'price': 5000,
                    'payed': False,
                    'Services': [
                        {
                            'descr': "début service",
                            'price': 2000,
                            'estimated_date_offset': {
                                'months': 0,
                                'weeks': 0,
                                'days': 0, },
                            'junior_day': 1,
                            'senior_day': 3,
                            'payed': False,
                            'done': 0},
                        {
                            'descr': "mileu service",
                            'price': 2000,
                            'estimated_date_offset': {
                                'months': 0,
                                'weeks': 2,
                                'days': 0, },
                            'junior_day': 5,
                            'senior_day': 3,
                            'payed': False,
                            'done': 0},
                        {
                            'descr': "fin service",
                            'price': 1000,
                            'estimated_date_offset': {
                                'months': 1,
                                'weeks': 2,
                                'days': 0, },
                            'junior_day': 13,
                            'senior_day': 1,
                            'payed': False,
                            'done': 0},
                    ]},
            ]
    elif nb_contract == 2:
        if lic:
            return [
                {
                    'description': "License_1_Contrat_2",
                    'start_date_offset': {
                        'months': 0,
                        'weeks': 0,
                        'days': 0, },
                    'duration': 12,
                    'price': 20000,
                    'payed': False},
                {
                    'description': "License_2_Contrat_2",
                    'start_date_offset': {
                        'months': 12,
                        'weeks': 0,
                        'days': 0, },
                    'duration': 9,
                    'price': 5000,
                    'payed': False},
            ]
        elif cons:
            return [
                {
                    'description': "Conseil_1_Contrat_2",
                    'start_date_offset': {
                        'months': 5,
                        'weeks': 0,
                        'days': 0, },
                    'duration': 2,
                    'price': 5000,
                    'payed': False,
                    'Services': [
                        {
                            'descr': "début service",
                            'price': 2000,
                            'estimated_date_offset': {
                                'months': 0,
                                'weeks': 0,
                                'days': 0, },
                            'junior_day': 1,
                            'senior_day': 3,
                            'payed': False,
                            'done': 0},
                        {
                            'descr': "mileu service",
                            'price': 2000,
                            'estimated_date_offset': {
                                'months': 2,
                                'weeks': 2,
                                'days': 0, },
                            'junior_day': 2,
                            'senior_day': 2,
                            'payed': False,
                            'done': 0},
                        {
                            'descr': "fin service",
                            'price': 1000,
                            'estimated_date_offset': {
                                'months': 4,
                                'weeks': 2,
                                'days': 0, },
                            'junior_day': 3,
                            'senior_day': 1,
                            'payed': False,
                            'done': 0},
                    ]},

                {
                    'description': "Conseil_2_Contrat_2",
                    'start_date_offset': {
                        'months': 12,
                        'weeks': 0,
                        'days': 0, },
                    'duration': 5,
                    'price': 5000,
                    'payed': False,
                    'Services': [
                        {
                            'descr': "début service",
                            'price': 2000,
                            'estimated_date_offset': {
                                'months': 0,
                                'weeks': 0,
                                'days': 0, },
                            'junior_day': 1,
                            'senior_day': 1,
                            'payed': False,
                            'done': 0},
                        {
                            'descr': "mileu service",
                            'price': 2000,
                            'estimated_date_offset': {
                                'months': 2,
                                'weeks': 2,
                                'days': 0, },
                            'junior_day': 2,
                            'senior_day': 2,
                            'payed': False,
                            'done': 0},
                        {
                            'descr': "fin service",
                            'price': 1000,
                            'estimated_date_offset': {
                                'months': 4,
                                'weeks': 2,
                                'days': 0, },
                            'junior_day': 3,
                            'senior_day': 3,
                            'payed': False,
                            'done': 0},
                    ]},

                {
                    'description': "Conseil_3_Contrat_2",
                    'start_date_offset': {
                        'months': 6,
                        'weeks': 0,
                        'days': 0, },
                    'duration': 5,
                    'price': 5000,
                    'payed': False,
                    'Services': [
                        {
                            'descr': "début service",
                            'price': 2000,
                            'estimated_date_offset': {
                                'months': 0,
                                'weeks': 0,
                                'days': 0, },
                            'junior_day': 3,
                            'senior_day': 1,
                            'payed': False,
                            'done': 0},
                        {
                            'descr': "mileu service",
                            'price': 2000,
                            'estimated_date_offset': {
                                'months': 2,
                                'weeks': 2,
                                'days': 0, },
                            'junior_day': 3,
                            'senior_day': 5,
                            'payed': False,
                            'done': 0},
                        {
                            'descr': "fin service",
                            'price': 1000,
                            'estimated_date_offset': {
                                'months': 4,
                                'weeks': 2,
                                'days': 0, },
                            'junior_day': 1,
                            'senior_day': 13,
                            'payed': False,
                            'done': 0},
                    ]},
            ]


def GetSpecificData(user, company_nb, DATA):
    return {
        'Company': DATA['Companies'][company_nb],
        'Contracts': [
            {
                'Client': "Client_1[Commercial 1]",
                'Commercial': "Commercial_%s_1" % user,
                'FactuManager': "Factu_%s" % user,
                'Descr': "Contrat_1_Client_1",
                'Start_date': GetDate(),
                'Duration': 12,
                'Facturation': 1,
                'Licenses': GetClient_1Data(nb_contract=1, lic=True),
                'Conseils': GetClient_1Data(nb_contract=1, cons=True),
            },

            {
                'Client': "Client_1[Commercial 1]",
                'Commercial': "Commercial_%s_1" % user,
                'FactuManager': "Factu_%s" % user,
                'Descr': "Contrat_2_Client_1",
                'Start_date': GetDate(),
                'Duration': 24,
                'Facturation': 1,
                'Licenses': GetClient_1Data(nb_contract=2, lic=True),
                'Conseils': GetClient_1Data(nb_contract=2, cons=True),
            },

            {
                'Client': "Client_2[Commercial 1]",
                'Commercial': "Commercial_%s_1" % user,
                'FactuManager': "Factu_%s" % user,
                'Descr': "Contrat_1_Client_2",
                'Start_date': GetDate(),
                'Duration': 12,
                'Facturation': 3,
                'Licenses': GetClient_1Data(nb_contract=1, lic=True),
                'Conseils': GetClient_1Data(nb_contract=1, cons=True),
            },

            {
                'Client': "Client_2[Commercial 1]",
                'Commercial': "Commercial_%s_1" % user,
                'FactuManager': "Factu_%s" % user,
                'Descr': "Contrat_2_Client_2",
                'Start_date': GetDate(),
                'Duration': 24,
                'Facturation': 3,
                'Licenses': GetClient_1Data(nb_contract=2, lic=True),
                'Conseils': GetClient_1Data(nb_contract=2, cons=True),
            },

            {
                'Client': "Client_3[Commercial 1]",
                'Commercial': "Commercial_%s_1" % user,
                'FactuManager': "Factu_%s" % user,
                'Descr': "Contrat_1_Client_3",
                'Start_date': GetDate(),
                'Duration': 12,
                'Facturation': 12,
                'Licenses': GetClient_1Data(nb_contract=1, lic=True),
                'Conseils': GetClient_1Data(nb_contract=1, cons=True),
            },

            {
                'Client': "Client_3[Commercial 1]",
                'Commercial': "Commercial_%s_1" % user,
                'FactuManager': "Factu_%s" % user,
                'Descr': "Contrat_2_Client_3",
                'Start_date': GetDate(),
                'Duration': 24,
                'Facturation': 12,
                'Licenses': GetClient_1Data(nb_contract=2, lic=True),
                'Conseils': GetClient_1Data(nb_contract=2, cons=True),
            },

            {
                'Client': "Client_1[Commercial 2]",
                'Commercial': "Commercial_%s_2" % user,
                'FactuManager': "Factu_%s" % user,
                'Descr': "Contrat_1_Client_1",
                'Start_date': GetDate() - relativedelta(months=3),
                'Duration': 12,
                'Facturation': 1,
                'Licenses': GetClient_1Data(nb_contract=1, lic=True),
                'Conseils': GetClient_1Data(nb_contract=1, cons=True),
            },

            {
                'Client': "Client_1[Commercial 2]",
                'Commercial': "Commercial_%s_2" % user,
                'FactuManager': "Factu_%s" % user,
                'Descr': "Contrat_2_Client_1",
                'Start_date': GetDate() - relativedelta(months=3),
                'Duration': 24,
                'Facturation': 1,
                'Licenses': GetClient_1Data(nb_contract=2, lic=True),
                'Conseils': GetClient_1Data(nb_contract=2, cons=True),
            },

            {
                'Client': "Client_2[Commercial 2]",
                'Commercial': "Commercial_%s_2" % user,
                'FactuManager': "Factu_%s" % user,
                'Descr': "Contrat_1_Client_2",
                'Start_date': GetDate() - relativedelta(months=3),
                'Duration': 12,
                'Facturation': 3,
                'Licenses': GetClient_1Data(nb_contract=1, lic=True),
                'Conseils': GetClient_1Data(nb_contract=1, cons=True),
            },

            {
                'Client': "Client_2[Commercial 2]",
                'Commercial': "Commercial_%s_2" % user,
                'FactuManager': "Factu_%s" % user,
                'Descr': "Contrat_2_Client_2",
                'Start_date': GetDate() - relativedelta(months=3),
                'Duration': 24,
                'Facturation': 3,
                'Licenses': GetClient_1Data(nb_contract=2, lic=True),
                'Conseils': GetClient_1Data(nb_contract=2, cons=True),
            },

            {
                'Client': "Client_3[Commercial 2]",
                'Commercial': "Commercial_%s_2" % user,
                'FactuManager': "Factu_%s" % user,
                'Descr': "Contrat_1_Client_3",
                'Start_date': GetDate() - relativedelta(months=3),
                'Duration': 12,
                'Facturation': 12,
                'Licenses': GetClient_1Data(nb_contract=1, lic=True),
                'Conseils': GetClient_1Data(nb_contract=1, cons=True),
            },

            {
                'Client': "Client_3[Commercial 2]",
                'Commercial': "Commercial_%s_2" % user,
                'FactuManager': "Factu_%s" % user,
                'Descr': "Contrat_2_Client_3",
                'Start_date': GetDate() - relativedelta(months=3),
                'Duration': 24,
                'Facturation': 12,
                'Licenses': GetClient_1Data(nb_contract=2, lic=True),
                'Conseils': GetClient_1Data(nb_contract=2, cons=True),
            },

            {
                'Client': "Client_1[Commercial 3]",
                'Commercial': "Commercial_%s_3" % user,
                'FactuManager': "Factu_%s" % user,
                'Descr': "Contrat_1_Client_1",
                'Start_date': GetDate() - relativedelta(months=6),
                'Duration': 12,
                'Facturation': 1,
                'Licenses': GetClient_1Data(nb_contract=1, lic=True),
                'Conseils': GetClient_1Data(nb_contract=1, cons=True),
            },

            {
                'Client': "Client_1[Commercial 3]",
                'Commercial': "Commercial_%s_3" % user,
                'FactuManager': "Factu_%s" % user,
                'Descr': "Contrat_2_Client_1",
                'Start_date': GetDate() - relativedelta(months=6),
                'Duration': 24,
                'Facturation': 1,
                'Licenses': GetClient_1Data(nb_contract=2, lic=True),
                'Conseils': GetClient_1Data(nb_contract=2, cons=True),
            },

            {
                'Client': "Client_2[Commercial 3]",
                'Commercial': "Commercial_%s_3" % user,
                'FactuManager': "Factu_%s" % user,
                'Descr': "Contrat_1_Client_2",
                'Start_date': GetDate() - relativedelta(months=6),
                'Duration': 12,
                'Facturation': 3,
                'Licenses': GetClient_1Data(nb_contract=1, lic=True),
                'Conseils': GetClient_1Data(nb_contract=1, cons=True),
            },

            {
                'Client': "Client_2[Commercial 3]",
                'Commercial': "Commercial_%s_3" % user,
                'FactuManager': "Factu_%s" % user,
                'Descr': "Contrat_2_Client_2",
                'Start_date': GetDate() - relativedelta(months=6),
                'Duration': 24,
                'Facturation': 3,
                'Licenses': GetClient_1Data(nb_contract=2, lic=True),
                'Conseils': GetClient_1Data(nb_contract=2, cons=True),
            },

            {
                'Client': "Client_3[Commercial 3]",
                'Commercial': "Commercial_%s_3" % user,
                'FactuManager': "Factu_%s" % user,
                'Descr': "Contrat_1_Client_3",
                'Start_date': GetDate() - relativedelta(months=6),
                'Duration': 12,
                'Facturation': 12,
                'Licenses': GetClient_1Data(nb_contract=1, lic=True),
                'Conseils': GetClient_1Data(nb_contract=1, cons=True),
            },

            {
                'Client': "Client_3[Commercial 3]",
                'Commercial': "Commercial_%s_3" % user,
                'FactuManager': "Factu_%s" % user,
                'Descr': "Contrat_2_Client_3",
                'Start_date': GetDate() - relativedelta(months=6),
                'Duration': 24,
                'Facturation': 12,
                'Licenses': GetClient_1Data(nb_contract=2, lic=True),
                'Conseils': GetClient_1Data(nb_contract=2, cons=True),
            },



        ],
    }


def get_data(DATA):
    return [GetSpecificData("Enis", 1, DATA),
            GetSpecificData("Eliot", 2, DATA),
            GetSpecificData("Damien", 3, DATA), ]


def CreateLicense(contract, LicenseData, license_index, dictio_license):
    date = LicenseData['start_date_offset']
    l = License(
        description=LicenseData['description'],
        price=LicenseData['price'],
        start_date=contract.start_date + relativedelta(
            months=date['months'],
            weeks=date['weeks'],
            days=date['days'],
        ),
        payed=LicenseData['payed'],
        duration=LicenseData['duration'],
        contract=contract,
    )
    l.save()
    # print(l, l.contract.start_date, date, l.start_date, l.end_date, l.duration)
    dictio_license[license_index] = l
    return l, license_index + 1


def CreateConseil(contract, ConseilData, conseil_index, dictio_conseil):
    date = ConseilData['start_date_offset']
    c = Conseil(
        description=ConseilData['description'],
        price=ConseilData['price'],
        start_date=contract.start_date + relativedelta(
            months=date['months'],
            weeks=date['weeks'],
            days=date['days'],
        ),
        duration=ConseilData['duration'],
        payed=ConseilData['payed'],
        contract=contract,
    )
    c.save()
    # print(c, c.contract.start_date, date, c.start_date, c.end_date, c.duration)
    dictio_conseil[conseil_index] = c
    return c, conseil_index + 1


def CreateService(conseil, ServiceData, service_index, dictio_service):
    date = ServiceData['estimated_date_offset']
    s = Service(
        description=ServiceData['descr'],
        estimated_date=conseil.start_date + relativedelta(
            months=date['months'],
            weeks=date['weeks'],
            days=date['days'],
        ),
        junior_day=ServiceData['junior_day'],
        senior_day=ServiceData['senior_day'],
        payed=ServiceData['payed'],
        done=ServiceData['done'],
        conseil=conseil,
    )
    s.save()
    # print(s, s.conseil.start_date, date, s.estimated_date, s.actual_date)
    dictio_service[service_index] = s
    return s, service_index + 1


def CreateContract(company, ContractData, contract_index, dictio_contract):
    try:
        client = company.client_set.get(
            name=ContractData['Client'])
        commercial = company.commercial_set.get(
            user__username=ContractData['Commercial'])
        factu_manager = company.manager_set.get(
            role=3,
            user__username=ContractData['FactuManager'])
    except Exception as e:
        print("in Create Contracts\n", ContractData, e)
        raise ValueError
    c = Contract(
        description=ContractData['Descr'],
        start_date=ContractData['Start_date'],
        duration=ContractData['Duration'],
        facturation=ContractData['Facturation'],
        company=company,
        client=client,
        commercial=commercial,
        factu_manager=factu_manager,
    )
    c.save()
    dictio_contract[contract_index] = c
    # print(c, date.today(), c.start_date, c.end_date, c.duration)
    return c, contract_index + 1


def CreateAllPresta(DATA):
    contract_index, license_index, conseil_index, service_index = 1, 1, 1, 1
    ContractCompanyDatas = get_data(DATA)

    for CompanyData in ContractCompanyDatas:
        try:
            company = CompanyData['Company']
            print(company)
            for ContractData in CompanyData['Contracts']:
                # print(ContractData)
                # print(contract_index)
                contract, contract_index = CreateContract(
                    company=company,
                    ContractData=ContractData,
                    contract_index=contract_index,
                    dictio_contract=DATA['Contracts']
                )
                # print(contract)
                for LicenseData in ContractData['Licenses']:
                    # print(LicenseData)
                    license_obj, license_index = CreateLicense(
                        contract=contract,
                        LicenseData=LicenseData,
                        license_index=license_index,
                        dictio_license=DATA['Licenses'],
                    )
                    # print(license_obj)
                for ConseilData in ContractData['Conseils']:
                    # print(ConseilData)
                    conseil, conseil_index = CreateConseil(
                        contract=contract,
                        ConseilData=ConseilData,
                        conseil_index=conseil_index,
                        dictio_conseil=DATA['Conseils'],
                    )
                    # print(conseil)
                    for ServiceData in ConseilData['Services']:
                        # print(ServiceData)
                        service, service_index = CreateService(
                            conseil=conseil,
                            ServiceData=ServiceData,
                            service_index=service_index,
                            dictio_service=DATA['Services'],
                        )
                        # print(service)
                    conseil.save()
        except ValueError:
            return
        except Exception as e:
            print("in Create All Contracts\n", e)
