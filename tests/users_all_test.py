
from src.auth import auth_login, auth_register
from src.other import users_all
import pytest
from src.error import InputError, AccessError

# Returns a list of all users and their associated details
def test_users_all1a():
    auth_register('HotGuy420@gmail.com', 'verySecureP@55word', 'Sylvester', 'Stallone') 
    user1_login = auth_login('HotGuy420@gmail.com', 'verySecureP@55word')
    user1_token = user1_login['token']

    assert(users_all(user1_token))

# Testing succes for a different tokens
def test_users_all1b():
    auth_register('C00LGUY@hotmail.com', 'aVeryC00lguy', 'Bruce', 'Willis')
    user1_login = auth_login('C00LGUY@hotmail.com', 'aVeryC00lguy')
    user1_token = user1_login['token']

    assert(users_all(user1_token))

# Testing succes for a different tokens
def test_users_all1c():
    auth_register('z9398627@unsw.edu.au', 'Shr3k15lyfe', 'Mickey', 'Mouse')
    user1_login = auth_login('z9398627@unsw.edu.au', 'Shr3k15lyfe')
    user1_token = user1_login['token']

    assert(users_all(user1_token))


