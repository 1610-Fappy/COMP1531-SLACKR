import re
from database import get_data
from helper_functions import decode_token, get_user, valid_token
from datetime import timezone, datetime

def query_search(token, query_str):
    data = get_data()
    if not valid_token(token):
        return "invalid token"
    user_id = decode_token(token)
    user_index = get_user(user_id)
    user = data['users'][user_index]

    search_list = []

    for channel in user['channels']:
        for channel_messages in channel['messages']:
            if re.search(query_str, channel_messages['message']):
                search_list.append(channel_messages)

    dt_now = datetime.utcnow()
    timestamp = int((dt_now - datetime(1970, 1, 1)).total_seconds())

    search_list_filter = list(filter(lambda m: m['time_created'] <= timestamp, search_list))
    search_list_sorted = sorted(search_list_filter, key=lambda k: k['time_created'], reverse=True)

    return { 
        'messages' : search_list_sorted
    }
