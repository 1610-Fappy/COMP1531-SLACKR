from src.auth import auth_register
from src.channels import channels_create
from src.error import InputError, AccessError
from src.channel import channel_addowner, channel_invite
import pytest

def channel_add_owner_testing():
    # Registering Users to later be put in channels
    User1 = auth_register('User1@gmail.com', 'User1Pa55', 'User', 'One')
    User2 = auth_register('User2@gmail.com', 'User2Pa55', 'User', 'Two')
    User3 = auth_register('User3@gmail.com', 'User3Pa55', 'User', 'Three')
    User4 = auth_register('User4@gmail.com', 'User4Pa55', 'User', 'Four')

    # Creating a channel which will be used to transfer ownership
    Channel1 = channels_create(User1['Token'], 'TransferOwnership', True)
    assert(channel_invite(User1['Token'], Channel1['channel_id'], User2['u_id']))
    assert(channel_invite(User1['Token'], Channel1['channel_id'], User3['u_id']))
    assert(channel_invite(User1['Token'], Channel1['channel_id'], User4['u_id']))
    assert(channel_addowner(User1['Token'], Channel1['channel_id'], User2['u_id']))

    # Producing error when channel_id is invalid
    with pytest.raises(InputError) as e:
        channel_addowner(User1['Token'], '-1', User2['u_id'])

    # Producing error when user is already an owner
    with pytest.raises(InputError) as e:
        channel_addowner(User1['Token'], Channel1['channel_id'], User2['u_id'])

    # Produce an access error when member tries to add someone as owner
    with pytest.raises(AccessError) as e:
        channel_addowner(User4['Token'], Channel1['channel_id'], User3['u_id'])