import re
from database import get_data
from helper_functions import decode_token, get_user, valid_token

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

    search_list_sorted = sorted(search_list, key=lambda k: k['time_created'], reverse=True)

    return { 'messages' : search_list_sorted}
