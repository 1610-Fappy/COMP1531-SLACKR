''' File to store data'''

USER = {
    'email' : None,
    'username' : None,
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
    'all_members' : []
}

DATA = {
    'users' : [],
    'active_tokens' : [],
    'channels' : []
}

def get_data():
    ''' Access global data from one point'''
    global DATA
    return DATA
