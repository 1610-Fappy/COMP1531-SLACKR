''' Contains functions for /user/'''
from database import get_data
from helper_functions import decode_token, get_user, valid_email, unused_email, valid_token

SECRET = 'HELLO'

def user_setname(token, name_first, name_last):
    ''' Function for user to change name'''
    data = get_data()
    check_token = valid_token(token)
    user_id = decode_token(token)
    check_valid_first_name = check_namelength(name_first)
    check_valid_last_name = check_namelength(name_last)
    if check_valid_first_name and check_valid_last_name and check_token:
        index = get_user(user_id)
        data['users'][index]['first_name'] = name_first
        data['users'][index]['last_name'] = name_last
    else:
        if not check_valid_first_name:
            return "invalid first name"
        if not check_valid_last_name:
            return "invalid last name"
        if not check_token:
            return "invalid token"
        

def user_setemail(token, email):
    ''' Function for user to change email'''
    data = get_data()
    check_token = valid_token(token)
    if not check_token:
        return "invalid token"
    user_id = decode_token(token)
    check_email_unused = unused_email(email)
    check_email_valid = valid_email(email)

    if check_email_unused and check_email_valid and check_token:
        index = get_user(user_id)
        data['users'][index]['email'] = email
        return
    if not check_email_valid:
        return "invalid email"
    if not check_email_unused:
        return "email used"

def user_sethandle(token, handle_str):
    ''' Function for user to change username'''
    data = get_data()
    check_token = valid_token(token)
    if not check_token:
        return "invalid token"

    user_id = decode_token(token)

    valid_handle = check_handlelength(handle_str)
    check_unused_handle = unused_handle(handle_str)

    if valid_handle and check_unused_handle and check_token:
        index = get_user(user_id)
        data['users'][index]['username'] = handle_str
        return
    if not valid_handle:
        return "invalid username"
    if not check_unused_handle:
        return "used username"

def user_profile(token, u_id):
    ''' Function to return users profile'''
    data = get_data()
    index = get_user(u_id)
    if valid_token(token) and index != -1:
        return data['users'][index]
    if index == -1:
        return "invalid u_id"
    return "invalid token"

def user_all(token):
    ''' Function that returns a list of all users and details'''
    data = get_data()
    if valid_token(token):
        return data['users']
    else:
        return "invalid token"

def check_handlelength(handle_str):
    ''' Checks that handle is within specified range'''
    handle_length = len(handle_str)
    if handle_length >= 2 and handle_length <= 20:
        return True
    else:
        print("Error for handle length")
        return False

def unused_handle(handle_str):
    ''' Checks that handle is not already used'''
    data = get_data()
    for user in data['users']:
        if user['username'] == handle_str:
            return False

    return True

def check_namelength(name):
    ''' Checks that name length is within specified range'''
    name_length = len(name)
    if name_length >= 1 and name_length <= 50:
        return True
    else:
        print("Error for name length")
        return False
