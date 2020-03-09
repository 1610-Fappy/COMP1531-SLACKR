from src.auth import auth_register
from src.channels import channels_create
from src.error import InputError, AccessError
from src.channel import channel_removeowner, channel_invite, channel_addowner
import pytest

def channel_remove_owner_testing():

    # Assume that channel_id and user_id are positive integers. Therefore negative integers in place of any _id will produce an error
    # Registering Users to later be put in channels
    User1 = auth_register('User1@gmail.com', 'User1Pa55', 'User', 'One')
    User2 = auth_register('User2@gmail.com', 'User2Pa55', 'User', 'Two')
    User3 = auth_register('User3@gmail.com', 'User3Pa55', 'User', 'Three')
    User4 = auth_register('User4@gmail.com', 'User4Pa55', 'User', 'Four')
    User5 = auth_register('User5@gmail.com', 'User5Pa55', 'User', 'Five')

    # Creating a channel which will be used to give ownership before removing
    Channel1 = channels_create(User1['Token'], 'TransferOwnership', True)
    assert(channel_invite(User1['Token'], Channel1['channel_id'], User2['u_id']))
    assert(channel_invite(User1['Token'], Channel1['channel_id'], User3['u_id']))
    assert(channel_invite(User1['Token'], Channel1['channel_id'], User4['u_id']))
    assert(channel_addowner(User1['Token'], Channel1['channel_id'], User2['u_id']))
    assert(channel_addowner(User1['Token'], Channel1['channel_id'], User3['u_id']))
    assert(channel_removeowner(User1['Token'], Channel1['channel_id'], User2['u_id']))

    # Produce InputError when removing User3 ownership from channel with invalid channel_id
    with pytest.raises(InputError) as e:
        channel_removeowner(User1['Token'], '-1', User3['u_id'])

    # Produce InputError when removing an owner who isnt an owner
    with pytest.raises(InputError) as e:
        channel_removeowner(User1['Token'], Channel1['channel_id'], User4['u_id'])

    # Produce AccessError when person removing ownership is not an owner
    with pytest.raises(AccessError) as e:
        channel_removeowner(User5['Token'], Channel1['channel_id'], User3['u_id'])

    # Produce AccessError when token passed is invalid
    with pytest.raises(AccessError) as e:
        channel_removeowner('InvalidToken', Channel1['channel_id'], User3['u_id'])