from src.auth import auth_register, auth_login, auth_logout
import pytest
from src.error import InputError

'''
ASSUMPTIONS
* 
'''


#ASSUME THAT REGISTER WORKS 
def test_login():
    user1Register = auth_register('HotGuy420@gmail.com', 'verySecureP@55word', 'Sylvester', 'Stallone') 
    user1Register_id = user1Register['u_id']
    auth_logout(user1Register['token'])

    user1Login = auth_login('HotGuy420@gmail.com', 'verySecureP@55word')
    user1Login_id = user1Login['u_id']

    assert user1Login_id == user1Register_id

    
    user2Register = auth_register('C00LGUY@hotmail.com', 'aVeryC00lguy', 'Bruce', 'Willis')
    user2Register_id = user2Register['u_id']
    auth_logout(user2Register['token'])

    user2Login = auth_login('c00LGUY@hotmail.com', 'aVeryC00lguy')
    user2Login_id = user2Login['u_id']

    assert user2Login_id == user2Register_id

    user3Register = auth_register('z9398627@unsw.edu.au', 'Shr3k15lyfe', 'Mickey', 'Mouse')
    user3Register_id = user3Register['u_id']
    auth_logout(user3Register['token'])

    user3Login = auth_login('z9398627@unsw.edu.au', 'Shr3k15lyfe')
    user3Login_id = user3Login['u_id']

    assert user3Login_id == user3Register_id

def test_loginPasswordIncorrect():

    user1 = auth_register('HotGuy420@gmail.com', 'verySecureP@55word', 'Sylvester', 'Stallone') 
    user2 = auth_register('C00LGUY@hotmail.com', 'aVeryC00lguy', 'Bruce', 'Willis')
    user3 = auth_register('z9398627@unsw.edu.au', 'Shr3k15lyfe', 'Mickey', 'Mouse')
    auth_logout(user1['token'])
    auth_logout(user2['token'])
    auth_logout(user3['token'])

    with pytest.raises(InputError) as e:
        auth_login('HotGuy420@gmail.com', 'wrongpass')

    with pytest.raises(InputError) as e:
        auth_login('C00LGUY@hotmail.com', 'wrongpass')

    with pytest.raises(InputError) as e:
        auth_login('z9398627', 'wrongpass')

def test_loginValidEmail():

#testing for Correct Format
with pytest.raises(InputError) as e:
    auth_login('lobo.com', 'P@ssw0rd')

with pytest.raises(InputError) as e:
    auth_login('popo@mail.com', 'P@ssw0rd')

#Testing for no ' ' in someone, with email in format someone@domain.com
with pytest.raises(InputError) as e:
    auth_login('king kong@gmail.com', 'P@ssw0rd')

#Testing for valid domain
with pytest.raises(InputError) as e:
    auth_login('poopmaster@cooldomn123.com', 'P@ssword')