from helper_functions import valid_token, valid_channelid, get_channel
from helper_functions import decode_token, get_user, user_inchannel
from datetime import datetime, timedelta
from database import get_data
<<<<<<< HEAD

def standup_start(token, channel_id, length):
    data = get_data()
    time_finish = datetime.now() + timedelta(seconds=length + 1)
=======
from datetime import timezone, datetime
from messages import create_message_dict
from helper_functions import decode_token

def standup_start(token, channel_id, length):
    data = get_data()

    time_finish = datetime.utcnow() + timedelta(seconds=length)
    finish_timestamp = int((time_finish - datetime(1970, 1, 1)).total_seconds())

>>>>>>> server_messages
    if not valid_token(token):
        return "invalid token"
    if not valid_channelid(channel_id):
        return "invalid channel_id"
    channel_index = get_channel(channel_id)

<<<<<<< HEAD
    if not data['channels'][channel_index]['standup_finish']:
        data['channels'][channel_index]['standup_finish'] = time_finish
    elif datetime.now() > data['channels']['standup_finish']:
        data['channels'][channel_index]['standup_finish'] = time_finish
    else:
        return "standup already active"
    
    return {'time_finish' : time_finish}
=======
    u_id = decode_token(token)

    if not data['channels'][channel_index]['startup_active']:
        data['channels'][channel_index]['standup_finish'] = finish_timestamp
        data['channels'][channel_index]['standup_starter'] = u_id
        data['channels'][channel_index]['startup_active'] = True

        return {'time_finish' : finish_timestamp}

    if data['channels'][channel_index]['startup_active']:
        return "standup already active"
>>>>>>> server_messages

def standup_active(token, channel_id):
    data = get_data()
    if not valid_token(token):
        return "invalid token"
    if not valid_channelid(channel_id):
        return "invalid channel_id"
    channel_index = get_channel(channel_id)
    channel = data['channels'][channel_index]

    if not channel['startup_active']:
        return {'is_active' : False, 'time_finish' : None}

    dt_now = datetime.utcnow()
    timestamp = int((dt_now - datetime(1970, 1, 1)).total_seconds())

    if timestamp > channel['standup_finish']:
        return {'is_active' : False, 'time_finish' : None}

    if timestamp <= channel['standup_finish']:
        return {'is_active' : True, 'time_finish' : channel['standup_finish']}

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

    if channel['startup_active']:

        stand_up_msg = create_message_dict(data['users'][user_index]['u_id'], data['users'][user_index]['name_first'] + " " + data['users'][user_index]['name_last'] + " : " + message, channel['standup_finish'])
        channel['standup_messages'].append(stand_up_msg)

        return

    else:

        return "no active standup"
