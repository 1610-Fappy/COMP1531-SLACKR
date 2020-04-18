from helper_functions import valid_token, valid_channelid, get_channel
from helper_functions import decode_token, get_user, user_inchannel
from datetime import datetime, timedelta
from database import get_data

def standup_start(token, channel_id, length):
    data = get_data()
    time_finish = datetime.now() + timedelta(seconds=length + 1)
    if not valid_token(token):
        return "invalid token"
    if not valid_channelid(channel_id):
        return "invalid channel_id"
    if not valid_channelid(channel_id):
        return "invalid channel_id"
    channel_index = get_channel(channel_id)

    if not data['channels'][channel_index]['standup_finish']:
        data['channels'][channel_index]['standup_finish'] = time_finish
    elif datetime.now() > data['channels']['standup_finish']:
        data['channels'][channel_index]['standup_finish'] = time_finish
    
    return time_finish

def standup_active(token, channel_id):
    data = get_data()
    if not valid_token(token):
        return "invalid token"
    if not valid_channelid(channel_id):
        return "invalid channel_id"
    channel_index = get_channel(channel_id)
    channel = data['channels'][channel_index]

    if datetime.now() < channel['standup_finish']:
        return {'is_active' : True, 'time_finish' : channel['standup_finish']}
    else:
        return {'is_active' : False, 'time_finish' : None}

def standup_send(token, channel_id, message):
    data = get_data()
    if not valid_token(token):
        return "invalid token"
    if not valid_channelid(channel_id):
        return "invalid channel_id"
    if len(message) > 1000:
        return "More than 1000 characters"
    u_id = decode_token(token)
    user_index = get_user(u_id)
    channel_index = get_channel(channel_id)
    channel = data['channels'][channel_index]
    if not user_inchannel(user_index, channel_id):
        return "not member"

    if datetime.now() < channel['standup_finish']:
        channel['standup_messages'].append(message)
    else:
        return "no active standup"
