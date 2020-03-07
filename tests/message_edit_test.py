from src.auth import auth_login, auth_register
from src.channels import channels_create
from src.channel import channel_join, channel_details
from src.message import message_send, message_remove, message_edit
import pytest
from src.error import InputError, AccessError

# Given a message, update it's text with new text. 
def test_message_edit1a():

    # User 1 creates a channel
    auth_register('HotGuy420@gmail.com', 'verySecureP@55word', 'Sylvester', 'Stallone') 

    user1_login = auth_login('HotGuy420@gmail.com', 'verySecureP@55word')
    user1_token = user1_login['token']

    channel_1 = channels_create(user1_token, 'Channel 1', True)

    # User 1 sends a message in Channel 1
    test_message = "It Aint How Hard You Hit...Its How Hard You Can Get Hit and Keep Moving Forward. Its About How Much You Can Take And Keep Moving Forward"
    ID_of_message = message_send(user1_token, channel_1, test_message)

    edited_quote = "You, me, or nobody is gonna hit as hard as life. But it aint about how hard you hit. Its about how hard you can get hit and keep moving forward."

    # User 1 is able to edit a message in Channel 1 because they are the admin/owner
    assert(message_edit(user1_token, ID_of_message, edited_quote) == {})

# If the new message is an empty string, the message is deleted.
def test_message_edit1b():

    # User 1 creates a channel
    auth_register('HotGuy420@gmail.com', 'verySecureP@55word', 'Sylvester', 'Stallone') 

    user1_login = auth_login('HotGuy420@gmail.com', 'verySecureP@55word')
    user1_token = user1_login['token']

    channel_1 = channels_create(user1_token, 'Channel 1', True)

    # User 1 sends a message in Channel 1
    test_message = "It Aint How Hard You Hit...Its How Hard You Can Get Hit and Keep Moving Forward. Its About How Much You Can Take And Keep Moving Forward"
    ID_of_message = message_send(user1_token, channel_1, test_message)

    edited_quote = ""

    # User 1 is able to edit a message in Channel 1 because they are the admin/owner
    assert(message_edit(user1_token, ID_of_message, edited_quote) == {})
    if (edited_quote == ""):
        assert(message_remove(user1_token, ID_of_message) == {})

# AccessError when none of the following are true:
#     Message with message_id was sent by the authorised user making this request
#     The authorised user is an admin or owner of this channel or the slackr

#   AccessError if User 2 is not part of Channel 1 but tries to edit a message
def test_message_edit_except1a():
    # User 1 creates a channel
    auth_register('HotGuy420@gmail.com', 'verySecureP@55word', 'Sylvester', 'Stallone') 

    user1_login = auth_login('HotGuy420@gmail.com', 'verySecureP@55word')
    user1_token = user1_login['token']

    channel_1 = channels_create(user1_token, 'Channel 1', True)

    # User 1 sends a message in Channel 1
    test_message = "It Aint How Hard You Hit...Its How Hard You Can Get Hit and Keep Moving Forward. Its About How Much You Can Take And Keep Moving Forward"
    ID_of_message = message_send(user1_token, channel_1, test_message)

    # User 2 tries to edit User 1's message in Channel 1 but has not joined
    auth_register('C00LGUY@hotmail.com', 'aVeryC00lguy', 'Bruce', 'Willis')

    user2_login = auth_login('C00LGUY@hotmail.com', 'aVeryC00lguy')
    user2_token = user2_login['token']

    with pytest.raises(AccessError) as e:
        message_edit(user2_token, ID_of_message, "Die Hard 2020")


#   AccessError if User 2 is part of Channel 1, but did not create the message or is an admin/owner, therefore cannot edit
def test_message_edit_except1b():
    # User 1 creates a channel
    auth_register('HotGuy420@gmail.com', 'verySecureP@55word', 'Sylvester', 'Stallone') 

    user1_login = auth_login('HotGuy420@gmail.com', 'verySecureP@55word')
    user1_token = user1_login['token']

    channel_1 = channels_create(user1_token, 'Channel 1', True)

    # User 1 sends a message in Channel 1
    test_message = "It Aint How Hard You Hit...Its How Hard You Can Get Hit and Keep Moving Forward. Its About How Much You Can Take And Keep Moving Forward"
    ID_of_message = message_send(user1_token, channel_1, test_message)

    # User 2 tries to edit User 1's message in Channel 1 but is not an admin or owner
    auth_register('C00LGUY@hotmail.com', 'aVeryC00lguy', 'Bruce', 'Willis')

    user2_login = auth_login('C00LGUY@hotmail.com', 'aVeryC00lguy')
    user2_token = user2_login['token']

    channel_join(user2_token, channel_1)
    # Asuuming that new members do not automatically become admins/owners, AccessError should occur

    with pytest.raises(AccessError) as e:
        message_edit(user2_token, ID_of_message, "Die Hard is better than Rocky")