''' File to store data'''

USER = {
    'email' : None,
    'handle_str' : None,
    'u_id' : None,
    'password' : None,
    'first_name' : None,
    'last_name' : None,
    'channels' : []
}
CHANNEL = {
    'channel_name' : None,
    'channel_id' : None,
    'owner_members' : [],
    'all_members' : [],
    'is_public' : None,
    'message_id' : None
}

DATA = {
    'users' : [],
    'active_tokens' : [],
    'channels' : [],
    'messages' : []
}

MEMBER_DICT = { 
    'u_id': None, 
    'name_first': None, 
    'name_last': None
}

def get_data():
    ''' Access global data from one point'''
    global DATA
    return DATA
