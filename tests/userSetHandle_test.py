from src.error import InputError
from src.user import user_profile_sethandle
from src.auth import auth_register


def test_setHandle():

    user1 = auth_register('coolguy@gmail.com', 'hello1234', 'Great', 'Khali')
    user_profile_sethandle(user1['token'], 'thebigman')

    user2 = auth_register('goodestman@hotmail.com', 'hello1234', 'Jim', 'Carrey')
    user_profile_sethandle(user2['token'], 'funnyman')

    user3 = auth_register('overtime@gmail.com', 'hello1234', 'Light', 'Bulb')
    user_profile_sethandle(user3['token'], 'PixarLamp')

def test_invalidHandleLength():

    user1 = auth_register('poopman@gmail.com', 'hello1234', 'Poop', 'Nugget')
    with pytest.raises(InputError) as e:
        user_profile_sethandle(user1['token'], '')

    with pytest.raises(InputError) as e:
        user_profile_sethandle(user1['token'], 'Thishandlenameiswaytoolongwhatareyouthinking')

def test_handleUsed():
        
        user1 = auth_register('coolmanguy@gmail.com', 'hello1234', 'Raphael', 'Turtle')
        user_profile_sethandle(user1['token'], 'coolguy')

        user2 = auth_register('bioman@hotmail.com', 'hello1234', 'Master', 'Splinter')
        with pytest.raises(InputError) as e:
            user_profile_sethandle(user2['token'], 'coolguy')
