import string
import random
from helper_functions import registered_email
from database import get_data
from auth import valid_password, hash_pass

def password_request(email):
    data = get_data()
    if not registered_email(email):
        return "not a user"

    reset_code = generate_resetCode()
    data['reset_codes'].append({'reset_code' : reset_code, 'email' : email})
    return reset_code

def password_reset(reset_code, new_password):
    data = get_data()
    if not valid_password(new_password):
        return "invalid password"
    for reset_users in data['reset_codes']:
        if reset_code == reset_users['reset_codes']:
            data['reset_codes'].remove(reset_code)
            for user in data['users']:
                if reset_users['email'] == user['email']:
                    user['password'] = hash_pass(new_password)
                    return
    
    return "invalid reset code"   

def generate_resetCode():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(6))
