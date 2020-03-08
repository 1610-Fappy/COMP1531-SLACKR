from src.channel import channel_invite, channel_details
from src.channels import channels_create
from src.auth import auth_register, auth_login
from src.error import InputError, AccessError
import pytest

def testing_channel_invite():
    User1 = auth_register('C00lguy@gmail.com', 'SickoM0de', 'Sicko', 'Mode')
    User2 = auth_register('UnC00lguy@gmail.com', 'NotSick0Mode', 'NotSicko', 'Mode')
    User3 = auth_register('AlmostC00lguy@gmail.com', 'SlightS1ckoMode', 'SlightSicko', 'Mode')
    User4 = auth_register('NotRelated@gmail.com', '0utOfHere', 'Adopted', 'Cousin')
    User5 = auth_register('NotWelcome@gmail.com', 'Get0utNow', 'Bye', 'Bye')
    
    # Assume anyone can invite someone else to a channel
    Channel1 = channels_create(User1['Token'], 'Sicko Mode', False)
    channel_invite(User1['Token'], 'Sicko Mode', User2['u_id'])
    channel_invite(User2['Token'], 'Sicko Mode', User3['u_id'])
    
    # Invalid if channel_id does not exist
    with pytest.raises(InputError) as e:
        channel_invite(User3['Token'], '-1', User4['u_id'])
    # Invalid if u_id does not exist
    with pytest.raises(InputError) as e:
        channel_invite(User3['Token'], Channel1['channel_id'], '-1')
    # Person inviting is not a member of the channel
    # Check if user
    channel_details(User1['Token'], Channel1['channel_id'])
    
    with pytest.raises(AccessError) as e:
        channel_invite(User5['Token'], Channel1['channel_id'], User5['u_id'])
