''' Contains all functions that are used to authorise users'''
import hashlib
import re
import uuid
from helper_functions import generate_token, valid_name, check_username, correct_pass
from helper_functions import unused_email, valid_email
from database import get_data

def auth_login(email, password):
    ''' Logs in a user'''
    data = get_data()
    check_email = valid_email(email) and not unused_email(email)
    if check_email:
        check_password = correct_pass(email, hash_pass(password))
    else:
        return "invalid email"
    if check_password['correct?']:
        token = generate_token(get_userid(email))
        data['active_tokens'].append(token)
        return {
            'u_id' : check_password['user']['u_id'],
            'token' : token
        }
    else:
        return "invalid password"


def auth_register(email, password, name_first, name_last):
    ''' Registers a user'''
    data = get_data()
    check_email = unused_email(email) and valid_email(email)
    check_psswrd = valid_password(password)
    check_names = valid_name(name_first) and valid_name(name_last)
    if check_email and check_psswrd and check_names:
        user = get_user_dict(email, password, name_first, name_last)
        token = generate_token(user['u_id'])
        data['users'].append(user)
        data['active_tokens'].append(token)
        return {
            'u_id' : user['u_id'],
            'token' : token
        }
    elif not check_email:
        return "invalid email"
    elif not check_psswrd:
        return "invalid password"
    elif not check_names:
        return "invalid name_length"

def auth_logout(token):
    ''' Logs out a user and invalidates the token'''
    data = get_data()
    for user_token in data['users']:
        if user_token['token'] == token:
            data['active_tokens'].remove(token)
            return {
                'is_success' : True
            }
    return{
        'is_success' : False
    }

def get_userid(email):
    ''' Gets user id using email to search'''
    data = get_data()
    for user in data['users']:
        if email == user['email']:
            return user['u_id']

def get_user_dict(email, password, name_first, name_last):
    ''' Stores user details into dictionary'''
    user = {
        'email' : email,
        'username' : generate_username(name_first, name_last),
        'u_id' : generate_u_id(),
        'password' : hash_pass(password),
        'first_name' : name_first,
        'last_name' : name_last
    }
    return user

def generate_u_id():
    ''' Generates unique user id'''
    return uuid.uuid4()

def valid_password(password):
    ''' Checks that the password is valid'''
    passwrd_length = len(password)
    if re.search('[a-zA-Z]', password) and passwrd_length >= 6 and re.search('[0-9]', password):
        return True

    return False

def hash_pass(password):
    ''' Hashes password to be stored securely'''
    return hashlib.sha256(password.encode()).hexdigest()

def change_username(username, new_user):
    ''' Changes username'''
    i = 0
    while(new_user and not check_username(username)):
        username = username[:10] + str(i)
        i += 1
    return username

def generate_username(first_name, last_name):
    ''' Generates username for new user'''
    username = first_name + last_name
    username_length = len(username)

    if username_length <= 20:
        valid_username = check_username(username)
    else:
        username = username[:20]
        valid_username = check_username(username)

    if not valid_username:
        username = change_username(username, True)

    return username
