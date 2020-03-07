# channels_list(token) == { channels }

from src.auth import auth_login, auth_register
from src.channels import channels_create, channels_list
import pytest
from src.error import InputError, AccessError

# Provide a list of all channels (and their associated details) that the authorised user is part of
def test_channels_list1a():
    # User 1 creates 4 channels
    auth_register('HotGuy420@gmail.com', 'verySecureP@55word', 'Sylvester', 'Stallone') 

    user1_login = auth_login('HotGuy420@gmail.com', 'verySecureP@55word')
    user1_token = user1_login['token']

    channels_create(user1_token, 'Channel 1', True)
    channels_create(user1_token, 'Channel 2', True)
    channels_create(user1_token, 'Channel 3', True)
    channels_create(user1_token, 'Channel 4', True)

    # Test if function works
    assert(channels_list(user1_token))

    # Confirm channel name in memory, matches name given by User 1
    channel_index = channels_list(user1_token)
    address_of_channels = channel_index['channels']
    first_channel = address_of_channels[0]
    assert (first_channel['name'] == 'Channel 1')

    channel_index = channels_list(user1_token)
    address_of_channels = channel_index['channels']
    second_channel = address_of_channels[1]
    assert (second_channel['name'] == 'Channel 2')

    channel_index = channels_list(user1_token)
    address_of_channels = channel_index['channels']
    third_channel = address_of_channels[2]
    assert (third_channel['name'] == 'Channel 3')

    channel_index = channels_list(user1_token)
    address_of_channels = channel_index['channels']
    fourth_channel = address_of_channels[3]
    assert (fourth_channel['name'] == 'Channel 4')

# Testing that channels_list will show channels that only the user is apart of
def test_channels_list1b():
    # User 1 creates 4 channels
    auth_register('HotGuy420@gmail.com', 'verySecureP@55word', 'Sylvester', 'Stallone') 

    user1_login = auth_login('HotGuy420@gmail.com', 'verySecureP@55word')
    user1_token = user1_login['token']

    channel_1 = channels_create(user1_token, 'Channel 1', True)
    channel_2 = channels_create(user1_token, 'Channel 2', True)
    channels_create(user1_token, 'Channel 3', True)
    channels_create(user1_token, 'Channel 4', True)

    # User 2 logs in and joins Channel 1 and 2, but not 3 and 4
    auth_register('z9398627@unsw.edu.au', 'Shr3k15lyfe', 'Mickey', 'Mouse')

    user2_login = auth_login('z9398627@unsw.edu.au', 'Shr3k15lyfe')
    user2_token = user2_login['token']
    
    channel_join(user2_token, channel_1)
    channel_join(user2_token, channel_2)

    # User 2's list of channels should not be the same as User 1
    assert(channels_list(user2_token) != channels_list(user1_token))
    
# AccessError - invalid token
def test_channels_list_AccessError():
    # User 1 creates 4 channels
    auth_register('HotGuy420@gmail.com', 'verySecureP@55word', 'Sylvester', 'Stallone') 

    user1_login = auth_login('HotGuy420@gmail.com', 'verySecureP@55word')
    user1_token = user1_login['token']
    
    channels_create(user1_token, 'Channel 1', True)
    channels_create(user1_token, 'Channel 2', True)
    channels_create(user1_token, 'Channel 3', True)
    channels_create(user1_token, 'Channel 4', True)

    # Error thrown when token passed in channels_list is not a valid token
    with pytest.raises(AccessError) as e:
        channels_list('invalidtoken')


