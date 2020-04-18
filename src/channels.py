''' Contains functions for /channel/'''
from database import get_data
from helper_functions import valid_token, generate_channelid, get_user
from helper_functions import valid_channelid, get_channel, decode_token, user_inchannel
from helper_functions import get_member_dict
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

        new_member = create_member_dict(user_id, data['users'][user_index]['name_first'], data['users'][user_index]['name_last'])

        channel['owner_members'].append(new_member)
        channel['all_members'].append(new_member)
        
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

    new_member = create_member_dict(u_id, data['users'][user_index]['name_first'], data['users'][user_index]['name_last'])
    
    data['channels'][channel_index]['all_members'].append(new_member)
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
        new_member = create_member_dict(user_id, data['users'][user_index]['name_first'], data['users'][user_index]['name_last'])
        data['channels'][channel_index]['all_members'].append(new_member)
        data['users'][user_index]['channels'].append(data['channels'][channel_index])
        return
    
    return "not public"

def channel_details(token, channel_id):
    ''' Gives basic details about channel if user is apart of it'''
    data = get_data()

    if not valid_token(token):
        return "invalid token"
    if not valid_channelid(channel_id):
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

    user_dict_index = get_user(u_id)

    tokenis_owner = check_userowner(channel_id, token_user_id)
    newuseris_owner = check_userowner(channel_id, u_id)

    if tokenis_owner and not newuseris_owner:
        in_channel = user_inchannel(user_dict_index, channel_id)

        channel_index = get_channel(channel_id)

        new_owner = create_member_dict(u_id, data['users'][user_dict_index]['name_first'], data['users'][user_dict_index]['name_last'])

        data['channels'][channel_index]['owner_members'].append(new_owner)

        if not in_channel:
            data['channels'][channel_index]['all_members'].append(new_owner)
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

    tokenis_owner = check_userowner(channel_id, token_user_id)
    newuseris_owner = check_userowner(channel_id, u_id)

    if tokenis_owner and newuseris_owner:
        channel_index = get_channel(channel_id)

        remove_member = get_member_dict(channel_id, u_id)

        data['channels'][channel_index]['owner_members'].remove(remove_member)

    if not tokenis_owner:
        return "token user not owner"
    if not newuseris_owner:
        return "not owner"

def channel_leave(token, channel_id):
    ''' User leaves a channel '''
    data = get_data()
    if not valid_token(token):
        return "invalid token"
    if not valid_channelid(channel_id):
        return "invalid channel_id"

    channel_index = get_channel(channel_id)
    user_id = decode_token(token)
    user_index = get_user(user_id)

    channel = data['channels'][channel_index]
    user = data['users'][user_index]

    if channel in user['channels']:
        user['channels'].remove(channel)
        for member in channel['all_members']:
            if user_id == member['u_id']:
                channel['all_members'].remove(member)

        for member in channel['owner_members']:
            if user_id == member['u_id']:
                channel['owner_members'].remove(member)

    else:
        return "not member"


def get_channel_dict(name, is_public):
    ''' Stores channels details into dictionary'''
    channel = {
        'channel_name' : name,
        'channel_id' : generate_channelid(name),
        'owner_members' : [],
        'all_members' : [],
        'is_public' : is_public,
        'messages': []
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

def create_member_dict(u_id, name_first, name_last):
    ''' Stores member details in a dictionary'''
    member = {
        'u_id' : u_id,
        'name_first' : name_first,
        'name_last' : name_last,
    }
    return member
