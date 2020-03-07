from src.error import InputError
import pytest
from src.user import user_profile_setemail
from src.auth import auth_register

def test_setEmail():

    user1 = auth_register('coolguy@gmail.com', 'hello1234', 'Michael', 'Jordan')
    user_profile_setemail(user1['token'], 'bigguy@gmail.com')

    user2 = auth_register('spoolguy@hotmail.com', 'hello1234', 'Jason', 'Dabestani')
    user_profile_setemail(user2['token'], 'knight360@hotmail.com')

    user3 = auth_register('lebronJames@gmail.com', 'hello1234', 'Rahul', 'Submarine')
    user_profile_setemail(user3['token'], 'Stephcurry@gmail.com')

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