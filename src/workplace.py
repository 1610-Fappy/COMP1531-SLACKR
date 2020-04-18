from database import get_data
from helper_functions import decode_token, get_user
from helper_functions import valid_token

def reset_workplace():
    ''' Resets the data to base case '''
    data = get_data()
    data['users'] = []
    data['channels'] = []
    data['active_tokens'] = []

def change_permission(token, u_id, permission_id):
    ''' Changes the permissions of a user '''
    data = get_data()
    if not valid_token(token):
        return "invalid token"
    if permission_id != 1 or permission_id != 2:
        return "invalid permission_id"
    token_u_id = decode_token(token)
    token_user_index = get_user(token_u_id)
    new_user_index = get_user(u_id)
    if data['users'][token_user_index]['permissions'] != 1:
        return "invalid permissions"
    if new_user_index == -1:
        return "invalid u_id"

    data['users'][new_user_index]['permissions'] = permission_id

def remove_user(token, u_id):
    ''' Removes a user from the slackr '''
    data = get_data()
    if not valid_token(token):
        return "invalid token"
    token_u_id = decode_token(token)
    token_user_index = get_user(token_u_id)
    new_user_index = get_user(u_id)
    if data['users'][token_user_index]['permissions'] != 1:
        return "invalid permissions"
    if new_user_index == -1:
        return "invalid u_id"

    user = data['users'][new_user_index]
    for channels in data['channels']:
        for member in channels['all_members']:
            if user['u_id'] == member['u_id']:
                channels['all_members'].remove(member)
        for member in channels['owner_members']:
            if user['u_id'] == member['owner_members']:
                channels['owner_members'].remove(member)

    data['users'].remove(user)
