import re


def validateEmail(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    regex2 = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}[.]\w{2,3}$'
    if re.search(regex, email) or re.search(regex2, email):
        return True
    return False

def validatePhoneNumber(phone_number):
    regex = '^[0-9]*$'
    if re.search(regex, phone_number):
        return True
    return False