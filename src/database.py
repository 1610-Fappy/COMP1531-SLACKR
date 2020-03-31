''' File to store data'''

#user = {
#    'email' : email,
#    'username' : generate_username(name_first, name_last),
#    'u_id' : generate_u_id(),
#    'password' : hash_pass(password),
#    'first_name' : name_first,
#    'last_name' : name_last
# }

# channel = {
#   'channel_name' : channel_name,
#   'channel_id' : generate_channelid(channel_name),
#   'owner_members' : [],
#   'all_members' : []
# }

DATA = {
    'users' : [],
    'active_tokens' : [],
    'channels' : []
}

def get_data():
    ''' Access global data from one point'''
    global DATA
    return DATA
