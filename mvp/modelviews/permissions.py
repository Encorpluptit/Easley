PERMISSION_DENIED = f"Oups, une erreur est survenue ! " \
                    f"Vous n'avez peut-être pas accès à cette page ou celle-ci n'existe plus."


def createConseilLicense(user, contract):
    valid = contract.validated
    if is_commercial(user) and checkCommercial(user.commercial, contract) and not valid:
        return True
    elif is_manager(user) and checkCompany(user, contract.company) and user.manager.role != 3:
        return checkCompany(user, contract.company)
    else:
        return False


def updateConseilLicense(user, contract, cls):
    valid = contract.validated
    if is_commercial(user) and checkCommercial(user.commercial, contract) and not valid:
        return cls.contract.id == contract.id
    elif is_manager(user) and checkCompany(user, contract.company) and user.manager.role != 3:
        return cls.contract.id == contract.id
    else:
        return False


def detailsConseilLicense(user, contract, cls):
    if is_commercial(user) and checkCommercial(user.commercial, contract):
        return cls.contract.id == contract.id
    elif is_manager(user) and checkCompany(user, contract.company):
        return cls.contract.id == contract.id
    else:
        return False


def contractClient(user, company):
    if is_commercial(user):
        return True
    elif is_manager(user) and user.manager.role != 3:
        return checkCompany(user, contract.company)
    else:
        return False


def contractCreate(user, company):
    if is_commercial(user) and company == user.manager.company:
        return True
    elif is_manager(user) and user.manager.role != 3 and company == user.manager.company:
        return True
    else:
        return False


def contractUpdate(user, contract):
    if is_commercial(user) and checkCommercial(user.commercial, contract) and not contract.validated:
        return True
    elif is_manager(user) and user.manager.role != 3 and contract.company == user.manager.company:
        return True
    else:
        return False


def contractDetails(user, contract):
    if is_commercial(user) and checkCommercial(user.commercial, contract):
        return True
    elif is_manager(user) and contract.company == user.manager.company:
        return True
    else:
        return False


def is_commercial(user):
    return hasattr(user, 'commercial')


def is_manager(user):
    return hasattr(user, 'manager')


def checkCompany(user, company):
    if is_manager(user):
        return user.manager.company == company
    elif is_commercial(user):
        return user.commercial.company == company
    else:
        return False


def checkClient(user, client):
    if is_manager(user):
        return user.manager.company == client.company
    elif is_commercial(user):
        return user.commercial == client.commercial
    else:
        return False


def checkCommercial(commercial, contract):
    return contract.commercial == commercial
