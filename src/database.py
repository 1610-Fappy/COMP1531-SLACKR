# ''' File to store data'''

# USER = {
#     'email' : None,
#     'handle_str' : None,
#     'u_id' : None,
#     'password' : None,
#     'first_name' : None,
#     'last_name' : None,
#     'channels' : []
# }
# CHANNEL = {
#     'channel_name' : None,
#     'channel_id' : None,
#     'owner_members' : [],
#     'all_members' : [],
#     'is_public' : None,
#     'messages' : []
# }

DATA = {
    'users' : [],
    'active_tokens' : [],
    'channels' : [],
}

# MEMBER_DICT = { 
#     'u_id': None, 
#     'name_first': None, 
#     'name_last': None
# }

# MESSAGES = {
#     'message_id', None,
#     'u_id': None, 
#     'message': None, 
#     'time_created': None, 
#     'reacts': [], 
#     'is_pinned': None
# }

# REACTS = {
#     'react_id': 1, 
#     'u_ids': [], 
#     'is_this_user_reacted': False 
# }

def get_data():
    ''' Access global data from one point'''
    global DATA
    return DATA
