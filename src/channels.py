''' Contains functions for /channel/'''
from database import get_data
from helper_functions import valid_token, generate_channelid, get_user
from helper_functions import valid_channelid, get_channel, decode_token, user_inchannel
from auth import get_user_dict

def channel_create(token, name, is_public):
    ''' Creates a channel and returns its id'''
    data = get_data()
    if not valid_token(token):
        return "invalid token"
    name_length = len(name)
    user_id = decode_token(token)
    # user_index = get_user(user_id)
    if name_length <= 20:
        user_index = get_user(user_id)
        channel = get_channel_dict(name, is_public)
        # index = get_user(token)

        data['users'][user_index]['channels'].append(channel)
        data['channels'].append(channel)

        channel['owner_members'].append(data['users'][user_index]['username'])
        channel['all_members'].append(data['users'][user_index]['username'])
        
        return {'channel_id' : channel['channel_id']}
    
    return "invalid channel name_length"

def channel_invite(token, channel_id, u_id):
    ''' Invites a user to a channel'''
    data = get_data()
    if not valid_token(token):
        return "invalid token"
    elif not valid_channelid(channel_id):
        return "invalid channel_id"

    token_user_id = decode_token(token)
    token_user = get_user(token_user_id)

    user_index = get_user(u_id)

    channel_index = get_channel(channel_id)

    tokenuser_in_channel = user_inchannel(token_user, channel_id)
    user_in_channel = user_inchannel(user_index, channel_id)

    if user_index == -1:
        return "invalid u_id"
    if not tokenuser_in_channel:
        return "not member"
    if user_in_channel:
        return "already member"
    
    data['channels'][channel_index]['all_members'].append(data['users'][user_index]['username'])
    data['users'][user_index]['channels'].append(data['channels'][channel_index])

    return

def channel_join(token, channel_id):
    ''' User joins a channel'''
    data = get_data()
    if not valid_token(token):
        return "invalid token"
    if not valid_channelid(channel_id):
        return "invalid channel_id"

    channel_index = get_channel(channel_id)
    user_id = decode_token(token)
    user_index = get_user(user_id)
    if data['channels'][channel_index]['is_public']:
        data['channels'][channel_index]['all_members'].append(data['users'][user_index]['username'])
        data['users'][user_index]['channels'].append(data['channels'][channel_index])
        return
    
    return "not public"

def channel_details(token, channel_id):
    ''' Gives basic details about channel if user is apart of it'''
    data = get_data()
    if not valid_token(token):
        return "invalid token"
    elif not valid_channelid(channel_id):
        return "invalid channel_id"

    token_id = decode_token(token)
    user_index = get_user(token_id)
    channel_index = get_channel(channel_id)
    in_channel = user_inchannel(user_index, channel_id)

    if not in_channel:
        return "not member"

    return {
        'name' : data['channels'][channel_index]['channel_name'],
        'owner_members' : data['channels'][channel_index]['owner_members'],
        'all_members' : data['channels'][channel_index]['all_members']
    }

def channel_listall(token):
    ''' Lists all channels and their details'''
    data = get_data()
    if valid_token(token):
        return {'channels' : data['channels']}
    return "invalid token"

def channel_list(token):
    ''' List all channels user is apart of'''
    data = get_data()
    if not valid_token(token):
        return "invalid token"

    u_id = decode_token(token)
    user_index = get_user(u_id)
    return {'channels' : data['users'][user_index]['channels']}

def channel_addowner(token, channel_id, u_id):
    ''' Adds user as an owner of a channel'''
    data = get_data()
    if not valid_token(token):
        return "invalid token"
    if not valid_channelid(channel_id):
        return "invalid channel_id"

    token_user_id = decode_token(token)


    token_user_dict_index = get_user(token_user_id)
    token_user_dict = data['users'][token_user_dict_index]

    user_dict_index = get_user(u_id)
    user_dict = data['users'][user_dict_index]

    token_username = token_user_dict['username']
    username = user_dict['username']

    tokenis_owner = check_userowner(channel_id, token_username)
    newuseris_owner = check_userowner(channel_id, username)

    if tokenis_owner and not newuseris_owner:
        in_channel = user_inchannel(user_dict_index, channel_id)

        channel_index = get_channel(channel_id)

        data['channels'][channel_index]['owner_members'].append(data['users'][user_dict_index]['username'])

        if not in_channel:
            data['channels'][channel_index]['all_members'].append(data['users'][user_dict_index]['username'])
            return
        return

    if not tokenis_owner:
        return "not owner"
    if newuseris_owner:
        return "already owner"

def channel_removeowner(token, channel_id, u_id):
    ''' Removes user from being an owner of a channel'''
    data = get_data()
    if not valid_token(token):
        return "invalid token"
    if not valid_channelid(channel_id):
        return "invalid channel_id"

    token_user_id = decode_token(token)

    token_user_dict_index = get_user(token_user_id)
    token_user_dict = data['users'][token_user_dict_index]

    user_dict_index = get_user(u_id)
    user_dict = data['users'][user_dict_index]

    token_username = token_user_dict['username']
    username = user_dict['username']

    tokenis_owner = check_userowner(channel_id, token_username)
    newuseris_owner = check_userowner(channel_id, username)

    if tokenis_owner and newuseris_owner:
        channel_index = get_channel(channel_id)
        data['channels'][channel_index]['owner_members'].remove(data['users'][user_dict_index]['username'])
        # data['channels'][channel_index]['all_members'].remove(data['users'][user_dict_index]['username'])

    if not tokenis_owner:
        return "token user not owner"
    if not newuseris_owner:
        return "not owner"

def get_channel_dict(name, is_public):
    ''' Stores channels details into dictionary'''
    channel = {
        'channel_name' : name,
        'channel_id' : generate_channelid(name),
        'owner_members' : [],
        'all_members' : [],
        'is_public' : is_public
    }
    return channel

def check_userowner(channel_id, username):
    ''' Checks whether a user is an owner of channel'''
    data = get_data()
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for owners in channel['owner_members']:
                if owners == username:
                    return True

    return False