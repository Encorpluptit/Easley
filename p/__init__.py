from .dict_global import DATA
from .companies import CreateAllCompanies
from .commercials import CreateAllCommercials
from .clients import CreateAllClients
from .managers import CreateAllManagers
from .prestas import CreateAllPresta


def PrintGlobalDict(DATA):
    print("<----------------------------GLOBAL_DICT----------------------->")
    for key, value in DATA.items():
        print(key)
        print("%s\n" % value)
    print("<-------------------------------------------------------------->\n")


def wipe_database(DATA):
    for user in DATA["Users"].values():
        user.delete()
    for section in DATA.values():
        section.clear()


def create_database(DATA):
    try:
        CreateAllCompanies(DATA)
        CreateAllManagers(DATA)
        CreateAllCommercials(DATA)
        CreateAllClients(DATA)
        CreateAllPresta(DATA)

    except Exception as e:
        print(e)


def init():
    NfctTab = [
        ("c", create_database),
        ("w", wipe_database),
    ]
    user_input = input()
    while user_input != "x":
        for i in range(len(NfctTab)):
            if user_input == NfctTab[i][0]:
                NfctTab[i][1](DATA)
        PrintGlobalDict(DATA)
        user_input = input()
    wipe_database(DATA)
    PrintGlobalDict(DATA)


init()
