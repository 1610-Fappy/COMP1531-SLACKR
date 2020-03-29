''' General Helper Functions'''
import re
import jwt

SECRET = 'DaddyItachi'

def generate_token(user):
    ''' Generates a token for user with given email'''
    global SECRET
    encoded = jwt.encode(user['email'], SECRET, algorithm='HS256')
    return str(encoded)

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
