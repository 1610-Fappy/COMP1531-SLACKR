from src.error import InputError
import pytest
from src.user import user_profile_setname
from src.auth import auth_register

def test_changeFirstName():

    user1 = auth_register('knight360@gmail.com', 'hello1234', 'Michael', 'Jordan')
    user_profile_setname(user1['token'], 'Lebron', 'Jordan')

    user2 = auth_register('steph@hotmail.com', 'hello1234', 'Stephen', 'Curry')
    user_profile_setname(user2['token'], 'Lebron', 'Jordan')

    user3 = auth_register('coolguy@gmail.com', 'hello1234', 'Bomber', 'Man')
    user_profile_setname(user3['token'], 'Mr', 'Man')

def test_changeLastName():

    user1 = auth_register('knight360@gmail.com', 'hello1234', 'Michael', 'Jordan')
    user_profile_setname(user1['token'], 'Michael', 'Lebron')

    user2 = auth_register('steph@hotmail.com', 'hello1234', 'Stephen', 'Curry')
    user_profile_setname(user2['token'], 'Stephen', 'Lebron')

    user3 = auth_register('coolguy@gmail.com', 'hello1234', 'Bomber', 'Man')
    user_profile_setname(user3['token'], 'Bomber', 'Guy')

def test_invalidFirstName():

    user1 = auth_register('knight360@gmail.com', 'hello1234', 'Michael', 'Jordan')
    with pytest.raises(InputError) as e:
        user_profile_setname(user1['token'], '', 'Jordan')

    user2 = auth_register('steph@hotmail.com', 'hello1234', 'Stephen', 'Curry')
    with pytest.raises(InputError) as e:
        user_profile_setname(user2['token'], 'thisnameiswaytoolongwahtthehellareyouthinkingnaminmgyourkidsthis', 'Curry')

    #assume that name cant have numbers in it
    user3 = auth_register('coolguy@gmail.com', 'hello1234', 'Bomber', 'Man')
    with pytest.raises(InputError) as e:
        user_profile_setname(user3['token'], 'Bombe23213123123r', 'Man')

def test_invalidLastName():

    user1 = auth_register('knight360@gmail.com', 'hello1234', 'Michael', 'Jordan')
    with pytest.raises(InputError) as e:
        user_profile_setname(user1['token'], 'Michael', '')

    user2 = auth_register('steph@hotmail.com', 'hello1234', 'Stephen', 'Curry')
    with pytest.raises(InputError) as e:
        user_profile_setname(user2['token'], 'Stephen', 'thisnameiswaytotooolongwhatthehellwereyouthinkingnnamingthis')

    user3 = auth_register('coolguy@gmail.com', 'hello1234', 'Bomber', 'Man')
    with pytest.raises(InputError) as e:
        user_profile_setname(user3['token'], 'Bomber', 'Guy213123')