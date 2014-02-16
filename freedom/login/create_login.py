from pylytics.library import connection
from freedom.library.utilities import victorinox

table_name = 'users'

def create_login(info):
    first_name = info['first_name'].lower()
    last_name = info['last_name'].lower()
    phone = info['phone'].lower()
    email = info['email'].lower()
    password = info['password']

    encrypted_password = victorinox.encrypt(password) 

    find_user_query = "SELECT * from %s where email = '%s' "%(table_name, email)
    existing_user = connection.run_query('storage', find_user_query)

    if len(existing_user) > 0:
        return False

    else:
        query = "INSERT INTO %s (first_name, last_name, phone, email, password) \
        Values ('%s', '%s', '%s', '%s', '%s')"%(table_name, first_name, last_name, phone, email, encrypted_password)

        connection.run_query('storage',query)

        return True

def user_login(info):

    email = info['email'].lower()
    password = info['password']

    encrypted_password = victorinox.encrypt(password) 

    find_user_query = "SELECT * from %s where email = '%s' and password = '%s'"%(table_name, email, encrypted_password)
    existing_user = connection.run_query('storage', find_user_query)

    if len(existing_user) == 0:
        return False

    user_id = existing_user[0][0]
    first_name = existing_user[0][1]
    last_name = existing_user[0][2]

    current_user = {
                    'user_id':user_id,
                    'first_name':first_name,
                    'last_name':last_name
                    }

    return current_user

def create_session_id():
    victorinox.id_generator(400)
