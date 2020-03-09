from src.error import InputError, AccessError
import pytest
from src.user import user_profile_setemail
from src.auth import auth_register, auth_logout

#Testing that everything works when valid
def test_setEmail():

    user1 = auth_register('coolguy@gmail.com', 'hello1234', 'Michael', 'Jordan')
    assert(user_profile_setemail(user1['token'], 'bigguy@gmail.com'))

    user2 = auth_register('spoolguy@hotmail.com', 'hello1234', 'Jason', 'Dabestani')
    assert(user_profile_setemail(user2['token'], 'knight360@hotmail.com'))

    user3 = auth_register('lebronJames@gmail.com', 'hello1234', 'Rahul', 'Submarine')
    assert(user_profile_setemail(user3['token'], 'Stephcurry@gmail.com'))

#Testinmg when email is invalid for use
def test_invalidEmail():

    user1 = auth_register('coolguy@gmail.com', 'hello1234', 'Michael', 'Jordan')
    with pytest.raises(InputError) as e:
        user_profile_setemail(user1['token'], 'bigguy@com')

    user2 = auth_register('spoolguy@hotmail.com', 'hello1234', 'Jason', 'Dabestani')
    with pytest.raises(InputError) as e:
        user_profile_setemail(user2['token'], 'knight360@hot213mail.com')

    user3 = auth_register('lebronJames@gmail.com', 'hello1234', 'Rahul', 'Submarine')
    with pytest.raises(InputError) as e:
        user_profile_setemail(user3['token'], 'Stephcurry.com')

#Testing if the email is already in use
def test_emailUsed():

    user1 = auth_register('bigman@gmail.com', 'hello1234', 'Jason', 'Dabestani')
    user2 = auth_register('Lebron@hotmail.com', 'hello1234', 'Jono', 'Illagan')
    with pytest.raises(InputError) as e:
        user_profile_setemail(user2['token'], 'bigman@gmail.com')

    user3 = auth_register('fatman@gmail.com', 'hello1234', 'Michael', 'Song')
    with pytest.raises(InputError) as e:
        user_profile_setemail(user3['token'], 'Lebron@hotmail.com')

    with pytest.raises(InputError) as e:
        user_profile_setemail(user3['token'], 'bigman@gmail.com')

#Testing if the token is still valid
def test_validToken():

    user1 = auth_register('coolguy@gmail.com', 'hello1234', 'Michael', 'Jordan')
    auth_logout(user1['token'])
    with pytest.raises(AccessError) as e:
        user_profile_setemail(user1['token'], 'bigguy@gmail.com')

    user2 = auth_register('spoolguy@hotmail.com', 'hello1234', 'Jason', 'Dabestani')
    auth_logout(user2['token'])
    with pytest.raises(AccessError) as e:
        user_profile_setemail(user2['token'], 'knight360@hotmail.com')
    
    user3 = auth_register('lebronJames@gmail.com', 'hello1234', 'Rahul', 'Submarine')
    auth_logout(user3['token'])
    with pytest.raises(AccessError) as e:
        user_profile_setemail(user3['token'], 'Stephcurry@gmail.com')