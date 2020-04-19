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
    check_valid_email = valid_email(email) 
    check_unused_email = unused_email(email)
    if check_valid_email and not check_unused_email:
        check_password = correct_pass(email, hash_pass(password))
    else:
        if not check_valid_email:
            return "invalid email"
        if check_unused_email:
            return "unused email"
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
    check_valid_email = valid_email(email)
    check_unused_email = unused_email(email)
    check_psswrd = valid_password(password)
    check_first_name = valid_name(name_first)
    check_last_name = valid_name(name_last)
    if check_valid_email and check_psswrd and check_first_name and check_last_name and check_unused_email:
        user = get_user_dict(email, password, name_first, name_last)
        token = generate_token(user['u_id'])
        data['users'].append(user)
        data['active_tokens'].append(token)
        return {
            'u_id' : user['u_id'],
            'token' : token
        }
    if not check_valid_email:
        return "invalid email"
    if not check_unused_email:
        return "used email"
    if not check_psswrd:
        return "invalid password"
    if not check_first_name:
        return "invalid first name"
    if not check_last_name:
        return "invalid first name"

def auth_logout(token):
    ''' Logs out a user and invalidates the token'''
    data = get_data()
    for user_token in data['active_tokens']:
        if user_token == token:
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
    if email == "the_owner@gmail.com":
        permission_id = 1
    else:
        permission_id = 2
    
    user = {
        'email' : email,
        'handle_str' : generate_username(name_first, name_last),
        'u_id' : generate_u_id(),
        'password' : hash_pass(password),
        'name_first' : name_first,
        'name_last' : name_last,
        'channels': [],
        'permission_id' : permission_id
    }
    return user

def generate_u_id():
    ''' Generates unique user id'''
    return uuid.uuid4().int>>112

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
    