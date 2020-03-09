from src.auth import auth_register, auth_login
from src.channel import channel_leave, channel_invite
from src.channels import channels_create
import pytest
from src.error import InputError, AccessError

def channel_leave_testing():
    
    # Assume channel_id returns an integer that is positive
    # First register a user
    FirstUser = auth_register('FirstUser@gmail.com', 'TheF1rstUser', 'First', 'User')

    # Create new channel using FirstUser account
    NewChannel = channels_create(FirstUser['Token'], 'TheNewChannel', True)

    # Create more users that get invited to the channel
    SecondUser = auth_register('SecUser@gmail.com', 'TheSecUser2', 'Sec', 'User')
    ThirdUser = auth_register('ThirdUser@gmail.com', 'TheThirdH0kage', 'SanDaime', 'Hokage')
    channel_invite(FirstUser['Token'], NewChannel['channel_id'], SecondUser['u_id'])
    channel_invite(FirstUser['Token'], NewChannel['channel_id'], ThirdUser['u_id'])

    # SecondUser leaves channel no error should occur
    channel_leave(SecondUser['Token'], NewChannel['channel_id'])

    # Create fourth user that is not invited to channel
    FourthUser = auth_register('Fourth@gmail.com', 'Yell0wFlash', 'Minato', 'Namikaze')

    # User leaves channel with no valid channel_id
    with pytest.raises(InputError) as e:
        channel_leave(ThirdUser['Token'], '-1')

    # User is leaving a channel they are not a part of
    with pytest.raises(AccessError) as e:
        channel_leave(FourthUser['Token'], NewChannel['channel_id'])

    # More tests with different channels
    First = auth_register('First@gmail.com', 'Y0ndaime', 'Hashirama', 'Senju')
    Mokuton = channels_create(First['Token'], 'Mokuton', True)
    Second = auth_register('Second@gmail.com', 'N1daimeH', 'Tobirama', 'Senju')
    Fifth = auth_register('Fifth@gmail.com', 'Goda1meHokage', 'Tsunade', 'Senju')
    Sixth = auth_register('Sixth@gmail.com', 'R0kudaime', 'Kakashi', 'Hatake')
    channel_invite(First['Token'], Mokuton['channel_id'], Second['u_id'])
    channel_leave(Second['Token'], Mokuton['channel_id'])
    channel_invite(First['Token'], Mokuton['channel_id'], Fifth['u_id'])

    # Same test as InputError test above
    with pytest.raises(InputError) as e:
        channel_leave(Fifth['Token'], '-2')

    # Same test as AccessError test above
    with pytest.raises(AccessError) as e:
        channel_leave(Sixth['Token'], Mokuton['channel_id'])

    # Produce AccessError when token passed is invalid
    with pytest.raises(AccessError) as e:
        channel_leave('InvalidToken', Mokuton['channel_id'])