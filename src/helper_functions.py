''' General Helper Functions'''
import re
import jwt
from database import get_data

SECRET = 'DaddyItachi'

def generate_token(user_id):
    ''' Generates a token for user with given email'''
    global SECRET
    encoded = jwt.encode({'u_id' : user_id}, SECRET, algorithm='HS256')
    return str(encoded)

def generate_channelid(channel_name):
    ''' Generates a channel id for channel'''
    global SECRET
    encoded = jwt.encode({'channel_id' : channel_name}, SECRET, algorithm='HS256')
    return str(encoded)

def decode_token(token):
    ''' Decodes a token to access user details'''
    global SECRET
    decoded = jwt.decode(token, SECRET, algorithms='HS256')
    return str(decoded['u_id'])

def get_user(user_id):
    ''' Gets user using given u_id'''
    data = get_data()
    index = 0
    for user in data['user']:
        if user['u_id'] == user_id:
            return index
        index += 1
    return -1

def user_inchannel(user_index, channel_id):
    ''' Checks if user is within channel specified'''
    data = get_data()
    for channel in data['users'][user_index]['channels']:
        if channel['channel_id'] == channel_id:
            return True

    return False

def get_channel(channel_id):
    ''' Gets channel with given channel id'''
    data = get_data()
    index = 0
    for channel in data['channels']:
        if channel_id == channel['channel_id']:
            return index
        index += 1
    print("Else error for invalid channel_id")

def valid_token(token):
    ''' Checks if token is valid'''
    data = get_data()
    for active_token in data['active_tokens']:
        if token == active_token:
            return True

    return False

def valid_channelid(channel_id):
    ''' Checks if channel_id is valid'''
    data = get_data()
    for channel in data['channels']:
        if channel_id == channel['channel_id']:
            return True

    return False

def valid_name(name):
    ''' Checks that the name inputted is valid'''
    name_length = len(name)
    if 1 <= name_length <= 50:
        return True

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
