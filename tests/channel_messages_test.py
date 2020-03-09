# def channel_messages(token, channel_id, start):
#     return {
#         'messages': [
#             {
#                 'message_id': 1,
#                 'u_id': 1,
#                 'message': 'Hello world',
#                 'time_created': 1582426789,
#             }
#         ],
#         'start': 0,
#         'end': 

# channel_messages(token, channel_id, start) == { messages, start, end }

from src.auth import auth_login, auth_register
from src.channels import channels_create
from src.channel import channel_messages
from src.message import message_send
import pytest
from src.error import InputError, AccessError

# Given a Channel with ID channel_id that the authorised user is part of, return up 
# to 50 messages between index "start" and "start + 50". Message with index 0 is the 
# most recent message in the channel. This function returns a new index "end" which 
# is the value of "start + 50", or, if this function has returned the least recent 
# messages in the channel, returns -1 in "end" to indicate there are no more messages 
# to load after this return.
def test_channel_messages1():
    # User 1 creates a channel
    auth_register('HotGuy420@gmail.com', 'verySecureP@55word', 'Sylvester', 'Stallone') 

    user1_login = auth_login('HotGuy420@gmail.com', 'verySecureP@55word')
    user1_token = user1_login['token']

    channel_1 = channels_create(user1_token, 'Channel 1', True)

    # User 1 sends 251 messages in Channel 1 (each character == one message) e.g.
    # I
    #  
    # a
    # m ...
    test_message = "I am Walt Disney in disguise. We keep moving forward, opening new doors, and doing new things, because we're curious and curiosity keeps leading us down new paths. I only hope that we never lose sight of one thing — that it was all started by a mouse."
    for c in test_message:
        message_send(user1_token, channel_1, c)

    assert(channel_messages(user1_token, channel_1, 0))
    assert(channel_messages(user1_token, channel_1, 50))
    assert(channel_messages(user1_token, channel_1, 100))
    assert(channel_messages(user1_token, channel_1, 150))
    assert(channel_messages(user1_token, channel_1, 200))
    assert(channel_messages(user1_token, channel_1, 250))
    

# InputError when any of:
#   Channel ID is not a valid channel
#   start is greater than the total number of messages in the channel

# InputError when Channel ID is not a valid channel, i.e. does not exist
def test_channel_messages_except1a():
     # User 1 logs in
    auth_register('HotGuy420@gmail.com', 'verySecureP@55word', 'Sylvester', 'Stallone') 

    user1_login = auth_login('HotGuy420@gmail.com', 'verySecureP@55word')
    user1_token = user1_login['token']
    
    with pytest.raises(InputError) as e:
        channel_messages(user1_token, "378doesnotexist241", 0)

# InputError when start is greater than the total number of messages in the channel
def test_channel_messages_except1b():
    # User 1 creates a channel
    auth_register('HotGuy420@gmail.com', 'verySecureP@55word', 'Sylvester', 'Stallone') 

    user1_login = auth_login('HotGuy420@gmail.com', 'verySecureP@55word')
    user1_token = user1_login['token']

    channel_1 = channels_create(user1_token, 'Channel 1', True)

    # User 1 sends only 1 message in Channel 1
    test_message = "I am Walt Disney in disguise. We keep moving forward, opening new doors, and doing new things, because we're curious and curiosity keeps leading us down new paths. I only hope that we never lose sight of one thing — that it was all started by a mouse."
    message_send(user1_token, channel_1, c)
    
    # channel_messages fails when start is greater than the number of messages i.e. fails below because 50 > 1.
    with pytest.raises(InputError) as e:
        channel_messages(user1_token, channel_1, 50)

# AccessError when Authorised user is not a member of channel with channel_id
def test_channel_messages_except2a():
    # User 1 creates a channel
    auth_register('HotGuy420@gmail.com', 'verySecureP@55word', 'Sylvester', 'Stallone') 

    user1_login = auth_login('HotGuy420@gmail.com', 'verySecureP@55word')
    user1_token = user1_login['token']

    channel_1 = channels_create(user1_token, 'Channel 1', True)

    # User 1 sends a bunch of single character messages
    test_message = "I am Walt Disney in disguise. We keep moving forward, opening new doors, and doing new things, because we're curious and curiosity keeps leading us down new paths. I only hope that we never lose sight of one thing — that it was all started by a mouse."
    for c in test_message:
        message_send(user1_token, channel_1, c)

    # User 2 logs in 
    auth_register('C00LGUY@hotmail.com', 'aVeryC00lguy', 'Bruce', 'Willis')

    user2_login = auth_login('C00LGUY@hotmail.com', 'aVeryC00lguy')
    user2_token = user2_login['token']

    # channel_messages fails when User 2 is not a member of Channel 1
    with pytest.raises(AccessError) as e:
        channel_messages(user2_token, channel_1, 0)

# AccessError - invalid token
def test_channel_messages_AccessError():

    # User 1 creates a channel
    auth_register('HotGuy420@gmail.com', 'verySecureP@55word', 'Sylvester', 'Stallone') 

    user1_login = auth_login('HotGuy420@gmail.com', 'verySecureP@55word')
    user1_token = user1_login['token']

    channel_1 = channels_create(user1_token, 'Channel 1', True)

    # User 1 sends 1 message in Channel 1
    test_message = "I am Walt Disney in disguise. We keep moving forward, opening new doors, and doing new things, because we're curious and curiosity keeps leading us down new paths. I only hope that we never lose sight of one thing — that it was all started by a mouse."
    message_send(user1_token, channel_1, test_message)

    # Error thrown when token passed in channel_messages is not a valid token
    with pytest.raises(AccessError) as e:
        channel_messages('invalidtoken', channel_1, 0)