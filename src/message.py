''' Contains all functions for /messages '''
import uuid
from helper_functions import decode_token, get_user, user_inchannel
from helper_functions import valid_channelid, valid_token
from database import get_data
from channels import check_userowner

def message_send(token, channel_id, message):
    ''' Function for user to send a message'''
    data = get_data()
    message_dict = {}
    if len(message) > 1000:
        return "More than 1000 characters"
    if not valid_token(token):
        return "invalid token"
    if not valid_channelid(channel_id):
        return "invalid channel_id"
    user_id = decode_token(token)
    user_index = get_user(user_id)
    if not user_inchannel(user_index, channel_id):
        return "not member"
    message_id = generate_messageid()
    message_dict['message_id'] = message_id
    message_dict['content'] = message
    message_dict['u_id'] = user_id
    message_dict['channel_id'] = channel_id
    for channel in data['channels']:
        if channel_id == channel['channel_id']:
            channel['messages'].append(message_id)
            data['messages'].append(message_dict)
    return message_id

def message_remove(token, message_id):
    ''' function to remove message'''
    pass

def message_edit(token, message_id, message):
    ''' Function that allows user to edit message'''
    data = get_data()
    if not valid_token(token):
        return "invalid token"
    if not valid_messageid(message_id):
        return "invalid message_id"
    user_id = decode_token(token)
    user_index = get_user(user_id)
    username = data['users'][user_index]['username']
    message_index = get_message(message_id)
    message_dict = data['messages'][message_index]
    if message == '':
        message_remove(token, message_id)
    if not check_userowner(message_dict['channel_id'], username) or user_id != message_dict['u_id']:
        return "not authorised"

    message_dict['content'] = message

def generate_messageid():
    ''' generates a unique message id'''
    return str(uuid.uuid4())

def valid_messageid(message_id):
    ''' checks that a message id is valid'''
    data = get_data()
    for message in data['messages']:
        if message['message_id'] == message_id:
            return True

    return False

def get_message(message_id):
    ''' Gets dictionary containing message details'''
    data = get_data()
    for message in data['messages']:
        index = 0
        if message['message_id'] == message_id:
            return index 
        index += 1