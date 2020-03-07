from error import InputError
from src.user import user_profile
from src.auth import auth_register, auth_login
import pytest

def test_userProfile():

    auth_register('knight360@hotmail.com', 'KillerX123', 'Michael', 'Vo')
    user1Login = auth_login('knight360@hotmail.com', 'KillerX123')
    user1Profile = user_profile(user1Login['token'], user1Login['u_id'])

    