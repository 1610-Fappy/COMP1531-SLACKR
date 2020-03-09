from src.auth import auth_register, auth_login
from src.channels import channels_create
from src.channel import channel_invite, channel_details
from src.error import InputError, AccessError
import pytest

def channeldetails_testing():
    User1 = auth_register('User1@gmail.com', 'User1Pa55', 'User', 'One')
    User2 = auth_register('User2@gmail.com', 'User2Pa55', 'User', 'Two')
    
    # Creating a channel using User1
    User1Channel = channels_create(User1['Token'], 'User1Channel', True)

    # Adding User2 to the created channel
    channel_invite(User1['Token'], User1Channel['channel_id'], User2['u_id'])

    # Displaying channel details
    channel_details(User1['Token'], User1Channel['channel_id'])

    # Creating user that is not in server
    User3 = auth_register('User3@gmail.com', 'User3Pa55', 'User', 'Three')

    # Produce error because channel id is invalid
    with pytest.raises(InputError) as e:
        channel_details(User1['Token'], '-1')

    # Use User3 token to produce an access error because User 3 is not in channel
    with pytest.raises(AccessError) as e:
        channel_details(User3['Token'], User1Channel['channel_id'])