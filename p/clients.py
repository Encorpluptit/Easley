from mvp.models import Client, Commercial



def get_data(DATA):

    Enis = {
        'Company': DATA['Companies'][1],
        'Clients': [
            {
                'Name': "Client_1[Commercial 1]",
                'Commercial' : "Commercial_Enis_1",
                'AccountManager': "Account_Enis",},
            {
                'Name': "Client_2[Commercial 1]",
                'Commercial' : "Commercial_Enis_1",
                'AccountManager': "Account_Enis",},
            {
                'Name': "Client_3[Commercial 1]",
                'Commercial' : "Commercial_Enis_1",
                'AccountManager': "Account_Enis",},
            {
                'Name': "Client_1[Commercial 2]",
                'Commercial' : "Commercial_Enis_2",
                'AccountManager': "Account_Enis",},
            {
                'Name': "Client_2[Commercial 2]",
                'Commercial' : "Commercial_Enis_2",
                'AccountManager': "Account_Enis",},
            {
                'Name': "Client_3[Commercial 2]",
                'Commercial' : "Commercial_Enis_2",
                'AccountManager': "Account_Enis",},
            {
                'Name': "Client_1[Commercial 3]",
                'Commercial' : "Commercial_Enis_3",
                'AccountManager': "Account_Enis",},
            {
                'Name': "Client_2[Commercial 3]",
                'Commercial' : "Commercial_Enis_3",
                'AccountManager': "Account_Enis",},
            {
                'Name': "Client_3[Commercial 3]",
                'Commercial' : "Commercial_Enis_3",
                'AccountManager': "Account_Enis",},
        ],
    }

    Eliot = {
        'Company': DATA['Companies'][2],
        'Clients': [
            {
                'Name': "Client_1[Commercial 1]",
                'Commercial' : "Commercial_Eliot_1",
                'AccountManager': "Account_Eliot",},
            {
                'Name': "Client_2[Commercial 1]",
                'Commercial' : "Commercial_Eliot_1",
                'AccountManager': "Account_Eliot",},
            {
                'Name': "Client_3[Commercial 1]",
                'Commercial' : "Commercial_Eliot_1",
                'AccountManager': "Account_Eliot",},
            {
                'Name': "Client_1[Commercial 2]",
                'Commercial' : "Commercial_Eliot_2",
                'AccountManager': "Account_Eliot",},
            {
                'Name': "Client_2[Commercial 2]",
                'Commercial' : "Commercial_Eliot_2",
                'AccountManager': "Account_Eliot",},
            {
                'Name': "Client_3[Commercial 2]",
                'Commercial' : "Commercial_Eliot_2",
                'AccountManager': "Account_Eliot",},
            {
                'Name': "Client_1[Commercial 3]",
                'Commercial' : "Commercial_Eliot_3",
                'AccountManager': "Account_Eliot",},
            {
                'Name': "Client_2[Commercial 3]",
                'Commercial' : "Commercial_Eliot_3",
                'AccountManager': "Account_Eliot",},
            {
                'Name': "Client_3[Commercial 3]",
                'Commercial' : "Commercial_Eliot_3",
                'AccountManager': "Account_Eliot",},
        ],
    }

    Damien = {
        'Company': DATA['Companies'][3],
        'Clients': [
            {
                'Name': "Client_1[Commercial 1]",
                'Commercial' : "Commercial_Damien_1",
                'AccountManager': "Account_Damien",},
            {
                'Name': "Client_2[Commercial 1]",
                'Commercial' : "Commercial_Damien_1",
                'AccountManager': "Account_Damien",},
            {
                'Name': "Client_3[Commercial 1]",
                'Commercial' : "Commercial_Damien_1",
                'AccountManager': "Account_Damien",},
            {
                'Name': "Client_1[Commercial 2]",
                'Commercial' : "Commercial_Damien_2",
                'AccountManager': "Account_Damien",},
            {
                'Name': "Client_2[Commercial 2]",
                'Commercial' : "Commercial_Damien_2",
                'AccountManager': "Account_Damien",},
            {
                'Name': "Client_3[Commercial 2]",
                'Commercial' : "Commercial_Damien_2",
                'AccountManager': "Account_Damien",},
            {
                'Name': "Client_1[Commercial 3]",
                'Commercial' : "Commercial_Damien_3",
                'AccountManager': "Account_Damien",},
            {
                'Name': "Client_2[Commercial 3]",
                'Commercial' : "Commercial_Damien_3",
                'AccountManager': "Account_Damien",},
            {
                'Name': "Client_3[Commercial 3]",
                'Commercial' : "Commercial_Damien_3",
                'AccountManager': "Account_Damien",},
        ],
    }

    return [Enis, Eliot, Damien]



def CreateClient(commercial, name, dictio_client, account_manager, client_index):
    c = Client(
        name=name,
        email="%s@Client.fr" % name,
        commercial=commercial,
        company=commercial.company,
        account_manager=account_manager
    )
    c.save()
    dictio_client[client_index] = c
    return client_index + 1


def CreateAllClients(DATA):
    client_index = 1
    CompanyClientDatas = get_data(DATA)

    for CompanyData in CompanyClientDatas:
        company = CompanyData['Company']
        # print(company)
        for client in CompanyData['Clients']:
            try:
                commercial = company.commercial_set.get(
                    user__username=client['Commercial'])
                account_manager = company.manager_set.get(
                    role=2,
                    user__username=client['AccountManager'])
                # print(commercial, manager)
                client_index = CreateClient(
                    commercial=commercial,
                    name=client['Name'],
                    dictio_client=DATA['Clients'],
                    account_manager=account_manager,
                    client_index=client_index,
                )
            except Exception as e:
                print("in Create All Clients\n", e)
