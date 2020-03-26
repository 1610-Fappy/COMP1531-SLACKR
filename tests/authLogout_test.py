from src.error import AccessError
import pytest
from src.auth import auth_register, auth_logout

#Testing for valid logging out
def test_logout():

    user1 = auth_register('HotGuy420@gmail.com', 'verySecureP@55word', 'Sylvester', 'Stallone')
    user1Logout = auth_logout(user1)
    assert(user1Logout['is_success'] == True)

    user2 = auth_register('C00LGUY@hotmail.com', 'aVeryC00lguy', 'Bruce', 'Willis')
    user2Logout = auth_logout(user2)
    assert(user2Logout['is_success'] == True)

    user3 = auth_register('z9398627@unsw.edu.au', 'Shr3k15lyfe', 'Mickey', 'Mouse')
    user3Logout = auth_logout(user3)
    assert(user3Logout['is_success'] == True)

def test_invalidToken():

    user1 = auth_register('HotGuy420@gmail.com', 'verySecureP@55word', 'Sylvester', 'Stallone')
    auth_logout(user1['token'])
    with pytest.raises(AccessError) as e:
        auth_logout(user1['token'])

    user2 = auth_register('C00LGUY@hotmail.com', 'aVeryC00lguy', 'Bruce', 'Willis')
    auth_logout(user2['token'])
    with pytest.raises(AccessError) as e:
        auth_logout(user2['token'])

    user3 = auth_register('z9398627@unsw.edu.au', 'Shr3k15lyfe', 'Mickey', 'Mouse')
    auth_logout(user3['token'])
    with pytest.raises(AccessError) as e:
        auth_logout(user3['token'])



