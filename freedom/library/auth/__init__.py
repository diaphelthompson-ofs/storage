from flask.ext.login import UserMixin
from wtforms import Form, TextField, PasswordField, validators
from freedom.library.utilities import victorinox
from pylytics.library import connection

table_name = 'users'

class LoginForm(Form):
    username = TextField("Username")
    password = PasswordField('Password', [validators.Required()])


def ldap_fetch(uid=None, name=None, passwd=None):
    email = name
    password = passwd

    try:
        encrypted_password = victorinox.encrypt(password) 
    except:
        encrypted_password = ''

    find_user_query = "SELECT * from %s where email = '%s' and password = '%s'"%(table_name, email, encrypted_password)
    existing_user = connection.run_query('storage', find_user_query)

    userid = existing_user[0][0]
    first_name = existing_user[0][1]
    last_name = existing_user[0][2]

    current_user = {
                    'userid':userid,
                    'name':first_name,
                    'last_name':last_name
                    }

    if len(existing_user) == 0:
        return None

    else:
        return current_user

class User(UserMixin):
    def __init__(self, uid=None, name=None, passwd=None):
        self.active = False

        ldapres = ldap_fetch(uid=uid, name=name, passwd=passwd)
        if ldapres is not None:
            self.name = ldapres['name']
            self.id = ldapres['userid']
            self.active = True

    def is_active(self):
        return self.active

    def get_id(self):
        return self.id
