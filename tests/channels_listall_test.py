# channels_listall(token) == { channels }

from src.auth import auth_login, auth_register
from src.channels import channels_create, channels_list, channels_listall
import pytest
from src.error import InputError, AccessError

# Provide a list of all channels (and their associated details)
# ASSUMPTION: User 1 has global permissons - that of a slackr owner, who can view all channels.

# Testing if User 1 can view all the channels they made
def test_channels_listall1a():
    # User 1 creates 4 channel
    auth_register('HotGuy420@gmail.com', 'verySecureP@55word', 'Sylvester', 'Stallone') 

    user1_login = auth_login('HotGuy420@gmail.com', 'verySecureP@55word')
    user1_token = user1_login['token']

    channels_create(user1_token, 'Channel 1', True)
    channels_create(user1_token, 'Channel 2', True)
    channels_create(user1_token, 'Channel 3', True)
    channels_create(user1_token, 'Channel 4', True)

    # Test if function works
    assert(channels_listall(user1_token))

    # Confirm channel name in memory, matches name given by User 1
    channel_index = channels_listall(user1_token)
    address_of_channels = channel_index['channels']
    first_channel = address_of_channels[0]
    assert (first_channel['name'] == 'Channel 1')

    channel_index = channels_listall(user1_token)
    address_of_channels = channel_index['channels']
    second_channel = address_of_channels[1]
    assert (second_channel['name'] == 'Channel 2')

    channel_index = channels_listall(user1_token)
    address_of_channels = channel_index['channels']
    third_channel = address_of_channels[2]
    assert (third_channel['name'] == 'Channel 3')

    channel_index = channels_listall(user1_token)
    address_of_channels = channel_index['channels']
    fourth_channel = address_of_channels[3]
    assert (fourth_channel['name'] == 'Channel 4')

# Testing if User 1 can view 2 channels they made and 2 channels User 2 made.
def test_channels_listall1b():
    # User 1 creates 2 channels
    auth_register('HotGuy420@gmail.com', 'verySecureP@55word', 'Sylvester', 'Stallone') 

    user1_login = auth_login('HotGuy420@gmail.com', 'verySecureP@55word')
    user1_token = user1_login['token']

    channels_create(user1_token, 'Channel 1', True)
    channels_create(user1_token, 'Channel 2', True)

    # User 2 creates 2 channels
    auth_register('z9398627@unsw.edu.au', 'Shr3k15lyfe', 'Mickey', 'Mouse')

    user2_login = auth_login('z9398627@unsw.edu.au', 'Shr3k15lyfe')
    user2_token = user2_login['token']

    channels_create(user2_token, 'Channel 3', True)
    channels_create(user2_token, 'Channel 4', True)

    # Test if function works
    assert(channels_listall(user1_token))

    # Confirm User 1 can see all channels in memory by checking it matches the names User 1 and User 2 gave
    channel_index = channels_listall(user1_token)
    address_of_channels = channel_index['channels']
    first_channel = address_of_channels[0]
    assert (first_channel['name'] == 'Channel 1')

    channel_index = channels_listall(user1_token)
    address_of_channels = channel_index['channels']
    second_channel = address_of_channels[1]
    assert (second_channel['name'] == 'Channel 2')

    channel_index = channels_listall(user1_token)
    address_of_channels = channel_index['channels']
    third_channel = address_of_channels[2]
    assert (third_channel['name'] == 'Channel 3')

    channel_index = channels_listall(user1_token)
    address_of_channels = channel_index['channels']
    fourth_channel = address_of_channels[3]
    assert (fourth_channel['name'] == 'Channel 4')

# AccessError - invalid token
def test_channels_listall_AccessError():
    # User 1 creates 2 channels
    auth_register('HotGuy420@gmail.com', 'verySecureP@55word', 'Sylvester', 'Stallone') 

    user1_login = auth_login('HotGuy420@gmail.com', 'verySecureP@55word')
    user1_token = user1_login['token']
    
    channels_create(user1_token, 'Channel 1', True)
    channels_create(user1_token, 'Channel 2', True)

    # User 2 creates 2 channels
    auth_register('z9398627@unsw.edu.au', 'Shr3k15lyfe', 'Mickey', 'Mouse')

    user2_login = auth_login('z9398627@unsw.edu.au', 'Shr3k15lyfe')
    user2_token = user2_login['token']

    channels_create(user2_token, 'Channel 3', True)
    channels_create(user2_token, 'Channel 4', True)

    # Error thrown when token passed in channels_listall is not a valid token
    with pytest.raises(AccessError) as e:
        channels_listall('invalidtoken')
