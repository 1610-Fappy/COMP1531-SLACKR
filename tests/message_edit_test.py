from src.auth import auth_login, auth_register
from src.channels import channels_create
from src.channel import channel_join, channel_details, channel_addowner
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

# Testing if User 2 who is made admin/owner can edit a message
def test_message_edit1c():

    # User 1 creates a channel
    auth_register('HotGuy420@gmail.com', 'verySecureP@55word', 'Sylvester', 'Stallone') 

    user1_login = auth_login('HotGuy420@gmail.com', 'verySecureP@55word')
    user1_token = user1_login['token']

    channel_1 = channels_create(user1_token, 'Channel 1', True)

    # User 1 sends a message in Channel 1
    test_message = "It Aint How Hard You Hit...Its How Hard You Can Get Hit and Keep Moving Forward. Its About How Much You Can Take And Keep Moving Forward"
    ID_of_message = message_send(user1_token, channel_1, test_message)

    # User 2 logins, joins Channel 1 and is made admin/owner
    auth_register('C00LGUY@hotmail.com', 'aVeryC00lguy', 'Bruce', 'Willis')

    user2_login = auth_login('C00LGUY@hotmail.com', 'aVeryC00lguy')
    user2_token = user2_login['token']
    user2_id = user2_login['u_id']

    channel_join(user2_token, channel_1)
    channel_addowner(user1_token, channel_1, user2_id)

    # User 2 edits User 1's message and is able to because they are now an admin/owner
    edit_to = "Yippie-Kai-Yay..."
    assert(message_edit(user2_token, ID_of_message, edit_to) == {})

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

# Since messages can't be more than 1000 characters than an edited message should also follow this rule
# Produce InputError is message > 1000 characters
def test_message_edit_except2a():

    # User 1 creates a channel
    auth_register('HotGuy420@gmail.com', 'verySecureP@55word', 'Sylvester', 'Stallone') 

    user1_login = auth_login('HotGuy420@gmail.com', 'verySecureP@55word')
    user1_token = user1_login['token']

    channel_1 = channels_create(user1_token, 'Channel 1', True)

    # User 1 sends a message in Channel 1
    test_message = "It Aint How Hard You Hit...Its How Hard You Can Get Hit and Keep Moving Forward. Its About How Much You Can Take And Keep Moving Forward"
    ID_of_message = message_send(user1_token, channel_1, test_message)

    # InputError as User 1 tries to edit his message, into a message > 1000
    too_much_message = "Let me tell you something you already know. The world ain't all sunshine and rainbows. It's a very mean and nasty place, and I don't care how tough you are, it will beat you to your knees and keep you there permanently if you let it. You, me, or nobody is gonna hit as hard as life. But it ain't about how hard you hit. It's about how hard you can get hit and keep moving forward; how much you can take and keep moving forward. That's how winning is done! Now, if you know what you're worth, then go out and get what you're worth. But you gotta be willing to take the hits, and not pointing fingers saying you ain't where you wanna be because of him, or her, or anybody. Cowards do that and that ain't you. You're better than that! I'm always gonna love you, no matter what. No matter what happens. You're my son and you're my blood. You're the best thing in my life. But until you start believing in yourself, you ain't gonna have a life. Yes Yes Yes Yes Yes Yes Yes Yes Yes Yes Yes Yes Yes Yes Yes Y"
    with pytest.raises(InputError) as e:
        message_edit(user1_token, ID_of_message, too_much_message)