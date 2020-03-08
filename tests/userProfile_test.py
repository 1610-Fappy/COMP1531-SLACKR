from src.error import InputError, AccessError
from src.user import user_profile
from src.auth import auth_register, auth_login, auth_logout
import pytest

def test_userProfile():

    user1 = auth_register('knight360@hotmail.com', 'KillerX123', 'Michael', 'Vo')
    auth_logout(user1['token'])
    user1Login = auth_login('knight360@hotmail.com', 'KillerX123')
    user1Profile = user_profile(user1Login['token'], user1Login['u_id'])

    user2 = auth_register('killerabz@gmail.com', 'P@55word', 'Abdul', 'Kanj')
    auth_logout(user2['token'])
    user2Login = auth_login('killerabz@gmail.com', 'P@55word')
    user2Profile = user_profile(user2Login['token'], user2Login['u_id'])

    user3 = auth_register('mrman@cse.unsw.edu.au', 'hello21234', 'Big', 'Man')
    auth_logout(user3['token'])
    user3Login = auth_login('mrman@cse.unsw.edu.au', 'hello21234')
    user3Profile = user_profile(user3Login['token'], user3Login['u_id'])

def test_invalidID():

    user1 = auth_register('knight360@hotmail.com', 'KillerX123', 'Michael', 'Vo')
    auth_logout(user1['token'])
    user1Login = auth_login('knight360@hotmail.com', 'KillerX123')
    with pytest.raises(InputError) as e:
        user1Profile = user_profile(user1Login['token'], 'InvalidID')

    user2 = auth_register('killerabz@gmail.com', 'P@55word', 'Abdul', 'Kanj')
    auth_logout(user2['token'])
    user2Login = auth_login('killerabz@gmail.com', 'P@55word')
    with pytest.raises(InputError) as e:
        user2Profile = user_profile(user2Login['token'], 'InvalidID')

    user3 = auth_register('mrman@cse.unsw.edu.au', 'hello21234', 'Big', 'Man')
    auth_logout(user3['token'])
    user3Login = auth_login('mrman@cse.unsw.edu.au', 'hello21234')
    with pytest.raises(InputError) as e:
        user3Profile = user_profile(user3Login['token'], 'InvalidID')

def test_validToken():

    user1 = auth_register('knight360@hotmail.com', 'KillerX123', 'Michael', 'Vo')
    auth_logout(user1['token'])
    #Token is invalid after logging out
    with pytest.raises(InputError) as e:
        user1Profile = user_profile(user1Login['token'], user1['u_id'])

    user2 = auth_register('killerabz@gmail.com', 'P@55word', 'Abdul', 'Kanj')
    auth_logout(user2['token'])
    with pytest.raises(InputError) as e:
        user2Profile = user_profile(user2Login['token'], user2['u_id'])

    user3 = auth_register('mrman@cse.unsw.edu.au', 'hello21234', 'Big', 'Man')
    auth_logout(user3['token'])
    with pytest.raises(InputError) as e:
        user3Profile = user_profile(user3Login['token'], user3['u_id'])
