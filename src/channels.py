''' Contains functions for /channel/'''
from database import get_data
from helper_functions import valid_token, generate_channelid, get_user, valid_channelid, get_channel

def channel_create(token, name, is_public):
    ''' Creates a channel and returns its id'''
    data = get_data()
    name_length = len(name)
    if name_length <= 20 and valid_token(token):
        channel = get_channel_dict(name, is_public)
        index = get_user(token)
        channel['owner_members'].append(data['users'][index])
        channel['all_members'].append(data['users'][index])
        data['channels'].append(channel)
        return channel['channel_id']

def channel_listall(token):
    ''' Lists all channels and their details'''
    data = get_data()
    if valid_token(token):
        return data['channels']

def channel_addowner(token, channel_id, u_id):
    ''' Adds user as an owner of a channel'''
    data = get_data()
    token_user_id = decode_token(token)

    if valid_token(token) and valid_channelid(channel_id):
        user_index = get_user(u_id)
        channel_index = get_channel(channel_id)
        data['channels'][channel_index]['owner_members'].append(data['users'][user_index])

    #Add error for user adding not being an owner of the slackr
    #Check that user is not already an owner of the slackr

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

def check_userowner(channel_id, u_id):
    ''' Checks whether a user is an owner of channel'''