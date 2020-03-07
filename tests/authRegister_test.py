from src.auth import auth_register
import pytest
from src.error import InputError


'''
ASSUMPTIONS
* PASSWORD > 6 CHARS, AT LEAST: 1 char, 1 INTEGER
* IF EMAIL IN FORMAT SOMEONE@DOMAIN.COM, SOMEONE MUST NOT HAVE A ' ' BETWEEN ITS CHARACTERS
* NAMES WILL NOT HAVE DIGITS IN THEM
'''
def test_register():

    assert(auth_register('HotGuy420@gmail.com', 'verySecureP@55word', 'Sylvester', 'Stallone')) 

    assert(auth_register('C00LGUY@hotmail.com', 'aVeryC00lguy', 'Bruce', 'Willis'))

    assert(auth_register('z9398627@unsw.edu.au', 'Shr3k15lyfe', 'Mickey', 'Mouse'))

def test_registerShortPassword():

    with pytest.raises(InputError) as e:
        auth_register('bigman@gmail.com', '234', 'Rey', 'Mysterio')

    with pytest.raises(InputError) as e:
        auth_register('lolol@hotmail.com', 'shawt', 'Luke', 'Lewis')

    with pytest.raises(InputError) as e:
        auth_register('bomberman@unsw.edu.au', 'L0b8t', 'Marty', 'Liwanag')


#Testing that passwords follow our assumed format/required security requirements
def test_registerValidPassword():

    with pytest.raises(InputError) as e:
        auth_register('klipklop@gmail.com', 'poopiwdsdwads', 'Steve', 'Smith')
 
    with pytest.raises(InputError) as e:
        auth_register('lordofthering@hotmail.com', '2134534123', 'Frodo', 'Baggins')

    with pytest.raises(InputError) as e:
        auth_register('thegreatwizard@unsw.edu.au', 'YOUSHALLNOTPASS', 'Gandalf', 'Great')

def test_registerValidEmail():

    #Testing for valid format
    with pytest.raises(InputError) as e:
        auth_register('lobo.com', 'P@ssw0rd', 'Jonathan', 'Bi')

    with pytest.raises(InputError) as e:
        auth_register('popo@mail.com', 'P@ssw0rd', 'Abdul', 'Kanj')

    #Testing for no ' ' in someone, with email in format someone@domain.com
    with pytest.raises(InputError) as e:
        auth_register('king kong@gmail.com', 'P@ssw0rd', 'King', 'Kong')

    #Testing for valid domain
    with pytest.raises(InputError) as e:
        auth_register('poopmaster@cooldomn123.com', 'P@ssword', 'Adolf', 'Ziggler')


#Testing that Error raised when email already in use
def test_registerEmailUsed():


    user1 = auth_register('HotGuy420@gmail.com', 'verySecureP@55word', 'Sylvester', 'Stallone') 

    user2 = auth_register('C00LGUY@hotmail.com', 'aVeryC00lguy', 'Bruce', 'Willis')

    user3 = auth_register('z9398627@unsw.edu.au', 'Shr3k15lyfe', 'Mickey', 'Mouse')

    with pytest.raises(InputError) as e:
        user1_1 = auth_register('HotGuy420@gmail.com', 'lobo8008135', 'Hayden', 'Smith')

    with pytest.raises(InputError) as e:
        user2_1 = auth_register('C00LGUY@hotmail.com', 'KingJames23', 'Lebron', 'James')

    with pytest.raises(InputError) as e:
        user3_1 = auth_register('z9398627@unsw.edu.au', 'UKDrill0G', 'Stormzy', 'RapGod')

def test_registerFirstName():

    with pytest.raises(InputError) as e:
        auth_register('noname@gmail.com', 'GhostC4rt', '', 'Ghost')

    with pytest.raises(InputError) as e:
        auth_register('LongName@hotmail.com', 'Th3Longestname', 'Thelongestnameisonethatisunexpectedlylongandterrifying', 'Scary')

    #Testing that names are not written with digits in them
    with pytest.raises(InputError) as e:
        auth_register('numbername@unsw.edu.au', 'd1g1tNames', 'w3ird', 'name')

def test_registerLastName():

    with pytest.raises(InputError) as e:
        auth_register('nolastname@gmail.com', 'GhostC4rt', 'Ghost', '')

    with pytest.raises(InputError) as e:
        auth_register('LonglastName@hotmail.com', 'Th3Longestname', 'Howard', 'ThelongestnameisonethatisunexpectedlylongandterrifyinglyScary')

    #Testing that names are not written with digits in them
    with pytest.raises(InputError) as e:
        auth_register('numbername@unsw.edu.au', 'd1g1tNames', 'weird', 'n4me')

    