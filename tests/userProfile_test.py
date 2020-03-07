from error import InputError
from src.user import user_profile
from src.auth import auth_register, auth_login
import pytest

def test_userProfile():

    auth_register('knight360@hotmail.com', 'KillerX123', 'Michael', 'Vo')
    user1Login = auth_login('knight360@hotmail.com', 'KillerX123')
    user1Profile = user_profile(user1Login['token'], user1Login['u_id'])

    auth_register('killerabz@gmail.com', 'P@55word', 'Abdul', 'Kanj')
    user2Login = auth_login('killerabz@gmail.com', 'P@55word')
    user2Profile = user_profile(user2Login['token'], user2Login['u_id'])

    auth_register('mrman@cse.unsw.edu.au', 'hello21234', 'Big', 'Man')
    user3Login = auth_login('mrman@cse.unsw.edu.au', 'hello21234')
    user3Profile = user_profile(user3Login['token'], user3Login['u_id'])

def test_invalidID():

    auth_register('knight360@hotmail.com', 'KillerX123', 'Michael', 'Vo')
    user1Login = auth_login('knight360@hotmail.com', 'KillerX123')
    with pytest.raises(InputError) as e:
        user1Profile = user_profile(user1Login['token'], 'InvalidID')

    auth_register('killerabz@gmail.com', 'P@55word', 'Abdul', 'Kanj')
    user2Login = auth_login('killerabz@gmail.com', 'P@55word')
    with pytest.raises(InputError) as e:
        user2Profile = user_profile(user2Login['token'], 'InvalidID')

    auth_register('mrman@cse.unsw.edu.au', 'hello21234', 'Big', 'Man')
    user3Login = auth_login('mrman@cse.unsw.edu.au', 'hello21234')
    with pytest.raises(InputError) as e:
        user3Profile = user_profile(user3Login['token'], 'InvalidID')
