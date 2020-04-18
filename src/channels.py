''' Contains functions for /channel/'''
from database import get_data
from helper_functions import valid_token, generate_channelid, get_user
from helper_functions import valid_channelid, get_channel, decode_token, user_inchannel

def channel_create(token, name, is_public):
    ''' Creates a channel and returns its id'''
    data = get_data()
    if not valid_token(token):
        return "invalid token"
    name_length = len(name)
    user_id = decode_token(token)
    user_index = get_user(user_id)
    if name_length <= 20:
        channel = get_channel_dict(name, is_public)
        index = get_user(token)
        channel['owner_members'].append(data['users'][index])
        channel['all_members'].append(data['users'][index])
        data['users'][user_index]['channels'].append(channel)
        data['channels'].append(channel)
        return {'channel_id' : channel['channel_id']}
    else:
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
    elif not tokenuser_in_channel:
        return "not member"
    elif user_in_channel:
        return "already member"
    else:
        data['channels'][channel_index]['all_members'].append(data['users'][user_index])
        data['users'][user_index]['channels'].append(data['channels'][channel_index])

def channel_join(token, channel_id):
    ''' User joins a channel'''
    data = get_data()
    if not valid_token(token):
        return "invalid token"
    elif not valid_channelid(channel_id):
        return "invalid channel_id"

    channel_index = get_channel(channel_id)
    user_id = decode_token(token)
    user_index = get_user(user_id)
    if data['channels'][channel_index]['is_public']:
        data['channels'][channel_index]['users'].append(data['users'][user_index])
        data['users'][user_index]['channels'].append(data['channels'][channel_index])
    else:
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
    else:
        return {
            'name' : data['channels'][channel_index]['name'],
            'owner_members' : data['channels'][channel_index]['owner_members'],
            'all_members' : data['channels'][channel_index]['all_members']
        }

def channel_listall(token):
    ''' Lists all channels and their details'''
    data = get_data()
    if valid_token(token):
        return {'channels' : data['channels']}

def channel_list(token):
    ''' List all channels user is apart of'''
    data = get_data()
    u_id = decode_token(token)
    user_index = get_user(u_id)
    return {'channels' : data['users'][user_index]['channels']}

def channel_addowner(token, channel_id, u_id):
    ''' Adds user as an owner of a channel'''
    data = get_data()
    if not valid_token(token):
        return "invalid token"
    elif not valid_channelid(channel_id):
        return "invalid channel_id"

    token_user_id = decode_token(token)
    tokenis_owner = check_userowner(channel_id, token_user_id)
    newuseris_owner = check_userowner(channel_id, u_id)

    if tokenis_owner and not newuseris_owner:
        user_index = get_user(u_id)
        in_channel = user_inchannel(user_index, channel_id)
        channel_index = get_channel(channel_id)
        data['channels'][channel_index]['owner_members'].append(data['users'][user_index])
        if not in_channel:
            data['channels'][channel_index]['all_members'].append(data['users'][user_index])

    elif not tokenis_owner:
        return "not owner"
    elif newuseris_owner:
        return "already owner"

def channel_removeowner(token, channel_id, u_id):
    ''' Removes user from being an owner of a channel'''
    data = get_data()
    if not valid_token(token):
        return "invalid token"
    elif not valid_channelid(channel_id):
        return "invalid channel_id"

    token_user_id = decode_token(token)
    tokenis_owner = check_userowner(channel_id, token_user_id)
    newuseris_owner = check_userowner(channel_id, u_id)

    if tokenis_owner and newuseris_owner:
        user_index = get_user(u_id)
        channel_index = get_channel(channel_id)
        data['channels'][channel_index]['owner_members'].remove(data['users'][user_index])
        data['channels'][channel_index]['all_members'].remove(data['users'][user_index])

    elif not tokenis_owner:
        return "not owner"
    elif not newuseris_owner:
        return "not owner"

def get_channel_dict(name, is_public):
    ''' Stores channels details into dictionary'''
    channel = {
        'channel_name' : name,
        'channel_id' : generate_channelid(name),
        'owner_members' : [],
        'all_members' : [],
        'is_public' : is_public,
        'standup_finish' : '',
        'standup_messages' : []
    }
    return channel

def check_userowner(channel_id, u_id):
    ''' Checks whether a user is an owner of channel'''
    data = get_data()
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for owners in channel['owner_members']:
                if owners['u_id'] == u_id:
                    return True

    return False
