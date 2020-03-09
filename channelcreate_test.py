from src.channel import channel_invite
from src.channels import channels_create
from src.auth import auth_register
import pytest
from src.error import InputError, AccessError


def test_channel_create():
    User1 = auth_register('User1@gmail.com', 'User1Pass', 'User', '1')
    User2 = auth_register('User2@gmail.com', 'User2Pass', 'User', '2')
    User5 = auth_register('C00lguy@gmail.com', 'MyAwes0mePa55word', 'Brock', 'Lesner')
    assert channels_create(User1['Token'], 'First Channel', True)
    assert channels_create(User2['Token'], 'Second Channel', False)
    assert channels_create(User5['Token'], 'SmackDownVSRaw', True)


    User3 = auth_register('User3@gmail.com', 'User3Pass', 'User', '3')
    with pytest.raises(InputError) as e:
        channels_create(User3['Token'], 'ThisChannelNameMightBeabittoolong', True)

    User4 = auth_register('User4@gmail.com', 'User4Pass', 'User', '4')
    with pytest.raises(InputError) as e:
        channels_create(User4['Token'], 'ThisChannelNameIsJus', True)

    Youtuber = auth_register('Youtube@gmail.com', 'MyYtAccountWillN0tBeHacked', 'You', 'Tube')
    with pytest.raises(InputError) as e:
        channels_create(Youtuber['Token'], 'MyChannel1sT00C001T0FitInTheLetterRestriction', True)

    # Produce AccessError when token passed is invalid
    with pytest.raises(AccessError) as e:
        channels_create('InvalidToken', 'MyAwesomeChannel', True)