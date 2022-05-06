"""
Account Class
"""
import base64
import re
import json


def password_checker(usr_password):
    HAS_AT_LEAST_THREE_KINDS_CHARS = re.compile("(?![a-z0-9]+$)")

    if len(usr_password) > 40:
        raise Exception("Invalid password(length)!", usr_password, len(usr_password))
    if usr_password.isspace():
        raise Exception("Invalid password(is space)!")
    if not HAS_AT_LEAST_THREE_KINDS_CHARS.search(usr_password):
        raise Exception("Invalid password(too simple)!")


def usr_name_checker(usr_name):
    ONLY_NUM_AND_LETTER = re.compile("^(?!\d+$)[\da-zA-Z_]+$")
    FIRST_CHAR_IS_LETTER = re.compile("^[a-zA-Z]")
    if len(usr_name) > 20:
        raise Exception("Invalid username(length)!", usr_name, len(usr_name))
    if usr_name.isspace():
        raise Exception("Invalid username(is space)!")
    if not ONLY_NUM_AND_LETTER.search(usr_name):
        raise Exception("Invalid username(special char)!", usr_name)
    if not FIRST_CHAR_IS_LETTER.search(usr_name):
        raise Exception("Invalid username(invalid first char)!", usr_name[0])


class Account:
    usr_name = ""
    usr_password_base64 = ""
    is_admin = False
    books_id = []

    def __init__(self, usr_name, usr_password, is_admin):
        self.register(usr_name, usr_password)
        self.is_admin = is_admin

    def register(self, usr_name, usr_password):
        try:
            usr_name_checker(usr_name)
            password_checker(usr_password)
        except Exception:
            raise Exception("Create Failed")
        else:
            self.usr_name = usr_name
            password_utf8 = usr_password.encode('utf-8')
            self.usr_password_base64 = base64.b64encode(password_utf8)

    def export_info(self):
        ret = {'username': self.usr_name, 'password': str(self.usr_password_base64), 'is_admin': self.is_admin, 'books': self.books_id}
        return ret


class AccountList(object):
    accounts = []
    def __init__(self):
        pass

    def load(self):
        with open('account.json', 'r') as acc_json:
            acc_dict = json.loads(acc_json.read())
        return acc_dict

    def register(self, usr_name, usr_password, is_admin):
        acc_dict = self.load()
        if usr_name in acc_dict:
            return False
        try:
            acc = Account(usr_name, usr_password, is_admin)
        except Exception:
            return False
        else:
            acc_dict[acc.usr_name] = acc.export_info()
            with open('account.json', 'w+') as acc_json:
                acc_json.write(json.dumps(acc_dict))
            return True

    def login(self, usr_name, usr_password):
        acc_dict = self.load()
        if usr_name not in acc_dict:
            return False
        else:
            if str(base64.b64encode(usr_password.encode('utf-8'))) == acc_dict[usr_name]['password']:
                return acc_dict[usr_name]
            else:
                return False

if __name__ == "__main__":
    acl = AccountList()
    print(acl.register('test', 'Tt1234', True))
    print(acl.login('test', 'Tt1234'))
