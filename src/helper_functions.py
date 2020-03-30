''' General Helper Functions'''
import re
import jwt
from database import get_data

SECRET = 'DaddyItachi'

def generate_token(user_id):
    ''' Generates a token for user with given email'''
    global SECRET
    encoded = jwt.encode({'u_id', user_id}, SECRET, algorithm='HS256')
    return str(encoded)

def decode_token(token):
    ''' Decodes a token to access user details'''
    global SECRET
    decoded = jwt.decode(token, SECRET, algorithms='HS256')
    return str(decoded)

def get_user(user_id):
    ''' Gets user using given u_id'''
    data = get_data()
    index = 0
    for user in data['user']:
        if user['u_id'] == user_id:
            return index
        index += 1
    print("else error for invalid user_id")

def valid_token(token):
    ''' Checks if token is valid'''
    data = get_data()
    for active_token in data['active_tokens']:
        if token == active_token:
            return True

    return False

def valid_name(name):
    ''' Checks that the name inputted is valid'''
    name_length = len(name)
    if name_length >= 1 and name_length <= 50:
        return True
    else:
        print("Error for name being too long")
        return False

def check_username(username):
    ''' Checks username is not already in use'''
    data = get_data()
    for handle in data['users']:
        if username == handle['username']:
            return False

    return True

def unused_email(email):
    ''' Checks whether email has already been registered to a user'''
    data = get_data()
    for users_email in data['users']:
        if email == users_email['email']:
            print("Error, email already in use")
            return False

    return True

def registered_email(email):
    ''' Checks whether email is registered to a user'''
    data = get_data()
    for users_email in data['users']:
        if email == users_email['email']:
            return True

    return False

def valid_email(email):
    ''' Checks that the email is valid format'''
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if re.search(regex, email):
        return True
    else:
        print("Invalid Email")
        return False

def correct_pass(email, password):
    ''' Checks whether the password entered is correct'''
    data = get_data()
    for user in data['users']:
        if email == user['email'] and password == user['password']:
            return {
                'user' : user,
                'correct?' : True
            }

    return {
        'correct?' : False
    }
