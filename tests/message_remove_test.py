from src.auth import auth_login, auth_register
from src.channels import channels_create
from src.channel import channel_join, channel_details
from src.message import message_send, message_remove
import pytest
from src.error import InputError, AccessError

# Given a message_id for a message, this message is removed from the channel
def test_message_remove():

    # User 1 creates a channel
    auth_register('HotGuy420@gmail.com', 'verySecureP@55word', 'Sylvester', 'Stallone') 

    user1_login = auth_login('HotGuy420@gmail.com', 'verySecureP@55word')
    user1_token = user1_login['token']

    channel_1 = channels_create(user1_token, 'Channel 1', True)

    # User 1 sends a message in Channel 1
    test_message = "It Aint How Hard You Hit...Its How Hard You Can Get Hit and Keep Moving Forward. Its About How Much You Can Take And Keep Moving Forward"
    ID_of_message = message_send(user1_token, channel_1, test_message)

    # User 1 is able to delete a message in Channel 1 because they are the admin/owner
    assert(message_remove(user1_token, ID_of_message) == {})

# InputError when any of: 
#   Message (based on ID) no longer exists
def test_message_remove_except1a():
    
    # User 1 creates a channel
    auth_register('HotGuy420@gmail.com', 'verySecureP@55word', 'Sylvester', 'Stallone') 

    user1_login = auth_login('HotGuy420@gmail.com', 'verySecureP@55word')
    user1_token = user1_login['token']

    channel_1 = channels_create(user1_token, 'Channel 1', True)

    # User 1 sends a message in Channel 1
    test_message = "It Aint How Hard You Hit...Its How Hard You Can Get Hit and Keep Moving Forward. Its About How Much You Can Take And Keep Moving Forward"
    ID_of_message = message_send(user1_token, channel_1, test_message)

    # User 1 removes a message in Channel 1
    message_remove(user1_token, ID_of_message)

    # User 1 tries to remove a message in Channel 1, that has already been removed. InputError should be produced.
    #InputError when the message is already removed
    with pytest.raises(InputError) as e:
        message_remove(user1_token, ID_of_message)

#   Trying to delete a message that doesn't exist
def test_message_remove_except1b():

    # User 1 creates a channel
    auth_register('HotGuy420@gmail.com', 'verySecureP@55word', 'Sylvester', 'Stallone') 

    user1_login = auth_login('HotGuy420@gmail.com', 'verySecureP@55word')
    user1_token = user1_login['token']

    channel_1 = channels_create(user1_token, 'Channel 1', True)

    does_not_exist = 56787654

    #InputError when the message User 1 tries to delete does not exist
    with pytest.raises(InputError) as e:
        message_remove(user1_token, does_not_exist)

# AccessError when none of the following are true:
#   Message with message_id was sent by the authorised user making this request
#   The authorised user is an admin or owner of this channel or the slackr

#   AccessError if User 2 is not part of Channel 1 but tries to delete a message
def test_message_remove_except2a():
    # User 1 creates a channel
    auth_register('HotGuy420@gmail.com', 'verySecureP@55word', 'Sylvester', 'Stallone') 

    user1_login = auth_login('HotGuy420@gmail.com', 'verySecureP@55word')
    user1_token = user1_login['token']

    channel_1 = channels_create(user1_token, 'Channel 1', True)

    # User 1 sends a message in Channel 1
    test_message = "It Aint How Hard You Hit...Its How Hard You Can Get Hit and Keep Moving Forward. Its About How Much You Can Take And Keep Moving Forward"
    ID_of_message = message_send(user1_token, channel_1, test_message)

    # User 2 tries to remove User 1's message in Channel 1 but has not joined
    auth_register('C00LGUY@hotmail.com', 'aVeryC00lguy', 'Bruce', 'Willis')

    user2_login = auth_login('C00LGUY@hotmail.com', 'aVeryC00lguy')
    user2_token = user2_login['token']

    with pytest.raises(AccessError) as e:
        message_remove(user2_token, ID_of_message)


#   AccessError if User 2 is part of Channel 1, but did not create the message or is an admin/owner, therefore cannot edit
def test_message_remove_except2b():
    # User 1 creates a channel
    auth_register('HotGuy420@gmail.com', 'verySecureP@55word', 'Sylvester', 'Stallone') 

    user1_login = auth_login('HotGuy420@gmail.com', 'verySecureP@55word')
    user1_token = user1_login['token']

    channel_1 = channels_create(user1_token, 'Channel 1', True)

    # User 1 sends a message in Channel 1
    test_message = "It Aint How Hard You Hit...Its How Hard You Can Get Hit and Keep Moving Forward. Its About How Much You Can Take And Keep Moving Forward"
    ID_of_message = message_send(user1_token, channel_1, test_message)

    # User 2 tries to remove User 1's message in Channel 1 but is not an admin or owner
    auth_register('C00LGUY@hotmail.com', 'aVeryC00lguy', 'Bruce', 'Willis')

    user2_login = auth_login('C00LGUY@hotmail.com', 'aVeryC00lguy')
    user2_token = user2_login['token']

    channel_join(user2_token, channel_1)
    # Asuuming that new members do not automatically become admins/owners, AccessError should occur

    # or use channel_details
    # channel_1_details = channel_details(user2_token, channel_1)
    # channel_1_owners = channel_1_details['owner_members']

    # for (number_of_owners in range(0, len(channel_1_owners)):
    # channel_1_possible_owner = channel_1_owners[number_of_owners]
    # channel_1_possible_owner_id = channel_1_possible_owner['u_id']
    # user2_ID = user2_login['u_id']
    #     if (user2_ID == channel_1_possible_owner_id):
    #         break

    # assert(user2_ID == channel_1_possible_owner_id)

    with pytest.raises(AccessError) as e:
        message_remove(user2_token, ID_of_message)

