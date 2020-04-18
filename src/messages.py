''' Contains all functions for /messages '''
import uuid
from helper_functions import decode_token, get_user, user_inchannel
from helper_functions import valid_channelid, valid_token
from database import get_data
from datetime import timezone, datetime

def message_send(token, channel_id, message):
    ''' Function for user to send a message'''
    data = get_data()

    if len(message) > 1000:
        return "more than 1000 characters"

    if not valid_token(token):
        return "invalid token"

    if not valid_channelid(channel_id):
        return "invalid channel_id"

    user_id = decode_token(token)
    user_index = get_user(user_id)
    
    if not user_inchannel(user_index, channel_id):
        return "not member"

    dt_now = datetime.now()
    timestamp = dt_now.replace(tzinfo=timezone.utc).timestamp()

    new_message = create_message_dict(user_id, message, int(timestamp))

    for channel in data['channels']:
        if channel_id == channel['channel_id']:
            channel['messages'].append(new_message)
            print(channel)
    
    return new_message['message_id']

def message_sendlater(token, channel_id, message, time_sent):
    ''' Function for user to send a message at a later time'''
    data = get_data()
    if len(message) > 1000:
        return "more than 1000 characters"
    if not valid_token(token):
        return "invalid token"
    if not valid_channelid(channel_id):
        return "invalid channel_id"
    
    user_id = decode_token(token)
    user_index = get_user(user_id)

    if not user_inchannel(user_index, channel_id):
        return "not member"
    
    dt_now = datetime.now()
    timestamp = dt_now.replace(tzinfo=timezone.utc).timestamp()
    if timestamp > time_sent:
        return "time passed"

    new_message = create_message_dict(user_id, message, time_sent)

    for channel in data['channels']:
        if channel_id == channel['channel_id']:
            channel['messages'].append(new_message)
    
    return new_message['message_id']

def message_react(token, message_id, react_id):
    ''' Function for user to react to a message'''

    if not valid_token(token):
        return "invalid token"
    
    if not valid_message_id(message_id):
        return "invalid message_id"

    if react_id != 1:
        return "invalid react_id"

    u_id = decode_token(token)

    message_dict = find_message(message_id)
    channel_dict = find_message_channel(message_id)
    for member in channel_dict['all_members']:
        if member['u_id'] == u_id:
            if not message_dict['reacts']:
                new_react = create_react_dict(react_id)
                new_react['u_ids'].append(u_id)
                message_dict['reacts'].append(new_react)
                return
            else:
                for react in message_dict['reacts']:
                    if react['react_id'] == react_id:
                        for reacted in react['u_ids']:
                            if reacted == u_id:
                                return "already reacted to"
                        react['u_ids'].append(u_id)
                        return

    return "not a member"

def message_unreact(token, message_id, react_id):
    ''' Function for user to unreact to a message'''

    if not valid_token(token):
        return "invalid token"
    
    if not valid_message_id(message_id):
        return "invalid message_id"

    if react_id != 1:
        return "invalid react_id"

    u_id = decode_token(token)

    message_dict = find_message(message_id)
    channel_dict = find_message_channel(message_id)
    for member in channel_dict['all_members']:
        if member['u_id'] == u_id:
            for react in message_dict['reacts']:
                if react['react_id'] == react_id:
                    for reacted in react['u_ids']:
                        if reacted == u_id:
                            react['u_ids'].remove(u_id)
                            if not react['u_ids']:
                                message_dict['reacts'].remove(react)
                            return
                    return "not reacted to"

    return "not a member"

def message_pin(token, message_id):
    ''' Function for user to pin a message'''

    if not valid_token(token):
        return "invalid token"
    
    if not valid_message_id(message_id):
        return "invalid message_id"

    message_dict = find_message(message_id)
    if message_dict['is_pinned']:
        return "already pinned"

    u_id = decode_token(token)
    channel_dict = find_message_channel(message_id)

    is_member = check_member(channel_dict, u_id)
    is_owner = check_owner(channel_dict, u_id)

    if not is_member:
        return "not member"
    if not is_owner:
        return "not owner"

    message_dict['is_pinned'] = True

    return

def message_unpin(token, message_id):
    ''' Function for user to unpin a message '''

    if not valid_token(token):
        return "invalid token"
    
    if not valid_message_id(message_id):
        return "invalid message_id"

    message_dict = find_message(message_id)
    if not message_dict['is_pinned']:
        return "already unpinned"

    u_id = decode_token(token)
    channel_dict = find_message_channel(message_id)

    is_member = check_member(channel_dict, u_id)
    is_owner = check_owner(channel_dict, u_id)

    if not is_member:
        return "not member"
    if not is_owner:
        return "not owner"

    message_dict['is_pinned'] = False

    return

def message_remove(token, message_id):
    ''' Function for user to remove a message '''

    if not valid_token(token):
        return "invalid token"
    
    if not valid_message_id(message_id):
        return "invalid message_id"

    message_dict = find_message(message_id)

    u_id = decode_token(token)
    channel_dict = find_message_channel(message_id)

    is_member = check_member(channel_dict, u_id)
    is_owner = check_owner(channel_dict, u_id)

    if not is_member:
        return "not member"
    if not is_owner:
        return "not owner"

    channel_dict['messages'].remove(message_dict)

    return

def message_edit(token, message_id, message):
    ''' Function for user to edit a message '''

    if len(message) > 1000:
        return "more than 1000 characters"

    if not valid_token(token):
        return "invalid token"

    if not valid_message_id(message_id):
        return "invalid message_id"

    message_dict = find_message(message_id)

    u_id = decode_token(token)
    channel_dict = find_message_channel(message_id)

    is_member = check_member(channel_dict, u_id)
    is_owner = check_owner(channel_dict, u_id)

    if not is_member:
        return "not member"
    if not is_owner:
        return "not owner"

    message_dict['message'] = message

    return
    
def channel_messages(token, channel_id, start):

    if not valid_token(token):
        return "invalid token"
    if not valid_channelid(channel_id):
        return "invalid channel_id"
    
    u_id = decode_token(token)

    channel_dict = find_channel_dict(channel_id)
    for user in channel_dict['all_members']:
        if user['u_id'] == u_id:
            user_in_channel = True
    
    if not user_in_channel:
        return "not member"

    list_of_messages = channel_dict['messages']

    end = start + 50
    if start > len(list_of_messages):
        return "start is greater than total messages"

    return {
        'messages': list_of_messages,
        'start': start,
        'end': end
    }

    

def generate_messageid():
    ''' Generates a unique message id'''
    return str(uuid.uuid4())

def valid_message_id(message_id):
    ''' Checks that a message id is valid'''
    data = get_data()
    for channel in data['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id:
                return True

    return False

def create_message_dict(u_id, message, time_created):
    ''' Creates message dictionary'''
    message_dict = {
    'message_id': generate_messageid(),
    'u_id': u_id,
    'message': message,
    'time_created': time_created,
    'reacts': [],
    'is_pinned': False
    }

    return message_dict

def use_user_dict(user_id):
    ''' Gets user using given u_id'''
    data = get_data()
    for user in data['users']:
        if user['u_id'] == user_id:
            return user
    return -1

def find_message(message_id):
    ''' Find dictionary of message given message_id'''
    data = get_data()
    for channel in data['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id:
                return message
    return None

def find_message_channel(message_id):
    ''' Find dictionary of channel given message_id'''
    data = get_data()
    for channel in data['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id:
                return channel
    return None

def create_react_dict(react_id):
    ''' Creates reaction dictionary'''

    react_dict = {
    'react_id': 1, 
    'u_ids': [], 
    'is_this_user_reacted': True 
    }

    return react_dict

def check_member(channel_dict, u_id):
    ''' Given channel dictionary checks is user is apart of channel'''
    for user in channel_dict['all_members']:
        if user['u_id'] == u_id:
            return True

    return False

def check_owner(channel_dict, u_id):
    ''' Given channel dictionary checks is user is owner of channel'''
    for user in channel_dict['owner_members']:
        if user['u_id'] == u_id:
            return True

    return False

def find_channel_dict(channel_id):
    ''' Given channel_id find corresponding channel dictionary'''
    data = get_data()

    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            return channel

    return None