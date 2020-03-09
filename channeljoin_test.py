from src.channel import channel_join
from src.auth import auth_register, auth_login
from src.channels import channels_create
from src.error import InputError, AccessError
import pytest

def testing_channel_join():
    User1 = auth_register('C00lguy@gmail.com', 'SickM0de', 'Sicko', 'Mode')
    User2 = auth_register('UnC00lguy@gmail.com', 'NotSick0Mode', 'NotSicko', 'Mode')
    channel1 = channels_create(User1['Token'], 'FirstChannel', True)
    PrivateChannel = channels_create(User1['Token'], 'MyPrivateChannel', False)
    channel_join(User2['Token'], channel1['channel_id'])

    # Channel id is not valid
    with pytest.raises(InputError) as e:
        channel_join(User2['Token'], '-1')
    
    # User2 trying to join a private channel
    with pytest.raises(AccessError) as e:
        channel_join(User2['Token'], PrivateChannel['channel_id'])

    CoolUser = auth_register('CoolUser@gmail.com', 'Pa55W0rd', 'Cool', 'User')
    NotSoCool = auth_register('WishIWasCool@gmail.com', 'BadPass1ame', 'NotSo', 'Cool')
    NewChannel = channels_create(CoolUser['Token'], 'PrivateChannel', False)

    # Joining channel with invalid channel id
    with pytest.raises(InputError) as e:
        channel_join(NotSoCool['Token'], '-1')

    # User tries to join private channel
    with pytest.raises(AccessError) as e:
        channel_join(NotSoCool['Token'], NewChannel['channel_id'])
    
    # Produce AccessError when token passed is invalid
    with pytest.raises(AccessError) as e:
        channel_join('InvalidToken', channel1['channel_id'])