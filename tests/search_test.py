# search(token, query_str) == { messages }

from src.auth import auth_login, auth_register
from src.other import users_all, search
from src.channel import channel_join
from src.channels import channels_create
from src.message import message_send
import pytest
from src.error import InputError, AccessError

# Given a query string, return a collection of messages in all of the channels that the user has joined that match the query
# Testing if owner can search own message
def test_search1a():
    # User 1 creates a channel
    auth_register('HotGuy420@gmail.com', 'verySecureP@55word', 'Sylvester', 'Stallone') 

    user1_login = auth_login('HotGuy420@gmail.com', 'verySecureP@55word')
    user1_token = user1_login['token']

    channel_1 = channels_create(user1_token, 'Channel 1', True)

    # User 1 sends a bunch of single character messages to Channel 1
    test_message = "I am Walt Disney in disguise. We keep moving forward, opening new doors, and doing new things, because we're curious and curiosity keeps leading us down new paths. I only hope that we never lose sight of one thing — that it was all started by a mouse."
    for c in test_message:
        message_send(user1_token, channel_1, c)

    # User 1 searches
    assert(search(user1_token, "m"))

# Testing if a user that joins a channel can search messages in it
def test_search1b():
    # User 1 creates a channel
    auth_register('HotGuy420@gmail.com', 'verySecureP@55word', 'Sylvester', 'Stallone') 

    user1_login = auth_login('HotGuy420@gmail.com', 'verySecureP@55word')
    user1_token = user1_login['token']

    channel_1 = channels_create(user1_token, 'Channel 1', True)

    # User 1 sends a bunch of single character messages to Channel 1
    test_message = "I am Walt Disney in disguise. We keep moving forward, opening new doors, and doing new things, because we're curious and curiosity keeps leading us down new paths. I only hope that we never lose sight of one thing — that it was all started by a mouse."
    for c in test_message:
        message_send(user1_token, channel_1, c)

    # User 2 logs in and joins Channel 1
    auth_register('z9398627@unsw.edu.au', 'Shr3k15lyfe', 'Mickey', 'Mouse')

    user2_login = auth_login('z9398627@unsw.edu.au', 'Shr3k15lyfe')
    user2_token = user2_login['token']
    
    channel_join(user2_login, channel_1)

    # User 2 searches
    assert(search(user2_token, "m"))

# AccessError - invalid token
def search_AccessError():
    # User 1 creates a channel
    auth_register('HotGuy420@gmail.com', 'verySecureP@55word', 'Sylvester', 'Stallone') 

    user1_login = auth_login('HotGuy420@gmail.com', 'verySecureP@55word')
    user1_token = user1_login['token']

    channel_1 = channels_create(user1_token, 'Channel 1', True)

    # User 1 sends a bunch of single character messages to Channel 1
    test_message = "I am Walt Disney in disguise. We keep moving forward, opening new doors, and doing new things, because we're curious and curiosity keeps leading us down new paths. I only hope that we never lose sight of one thing — that it was all started by a mouse."
    for c in test_message:
        message_send(user1_token, channel_1, c)

    # Error thrown when token passed in search is not a valid token
    with pytest.raises(AccessError) as e:
        search('invalidtoken', "m")

