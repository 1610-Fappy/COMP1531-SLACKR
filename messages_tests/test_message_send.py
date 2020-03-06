# reminder: remove _for_testing suffix
from auth_for_testing import auth_login, auth_register
from channels_for_testing import channels_create
from message_for_testing import message_send
import pytest
from error_for_testing import InputError, AccessError


# Send a message from authorised_user to the channel specified by channel_id
def test_message_send():

    # User 1 creates a channel
    auth_register('HotGuy420@gmail.com', 'verySecureP@55word', 'Sylvester', 'Stallone') 

    user1_login = auth_login('HotGuy420@gmail.com', 'verySecureP@55word')
    user1_token = user1_login['token']

    channel_1 = channels_create(user1_token, 'Channel 1', True)

    # User 1 sends a message in Channel 1
    test_message = "It Aint How Hard You Hit...Its How Hard You Can Get Hit and Keep Moving Forward. Its About How Much You Can Take And Keep Moving Forward"

    assert(message_send(user1_token, channel_1, test_message))

# InputError when any of: Message is more than 1000 characters ( > 1000)
def test_message_send_except1():

    # User 1 creates a channel
    auth_register('HotGuy420@gmail.com', 'verySecureP@55word', 'Sylvester', 'Stallone') 

    user1_login = auth_login('HotGuy420@gmail.com', 'verySecureP@55word')
    user1_token = user1_login['token']

    channel_1 = channels_create(user1_token, 'Channel 1', True)

    # test_message has 1001 characters
    # InputError as User1 tries to send a message > 1000
    test_message = "Let me tell you something you already know. The world ain't all sunshine and rainbows. It's a very mean and nasty place, and I don't care how tough you are, it will beat you to your knees and keep you there permanently if you let it. You, me, or nobody is gonna hit as hard as life. But it ain't about how hard you hit. It's about how hard you can get hit and keep moving forward; how much you can take and keep moving forward. That's how winning is done! Now, if you know what you're worth, then go out and get what you're worth. But you gotta be willing to take the hits, and not pointing fingers saying you ain't where you wanna be because of him, or her, or anybody. Cowards do that and that ain't you. You're better than that! I'm always gonna love you, no matter what. No matter what happens. You're my son and you're my blood. You're the best thing in my life. But until you start believing in yourself, you ain't gonna have a life. Yes Yes Yes Yes Yes Yes Yes Yes Yes Yes Yes Yes Yes Yes Yes Y"
    with pytest.raises(InputError) as e:
        message_send(user1_token, channel_1, test_message)

# AccessError when:  the authorised user has not joined the channel they are trying to post to
def test_message_send_except2():

    # User 1 creates a channel
    auth_register('HotGuy420@gmail.com', 'verySecureP@55word', 'Sylvester', 'Stallone') 

    user1_login = auth_login('HotGuy420@gmail.com', 'verySecureP@55word')
    user1_token = user1_login['token']

    channel_1 = channels_create(user1_token, 'Channel 1', True)

    # User 2 tries to send a message in Channel 1 but has not joined
    auth_register('C00LGUY@hotmail.com', 'aVeryC00lguy', 'Bruce', 'Willis')

    user2_login = auth_login('C00LGUY@hotmail.com', 'aVeryC00lguy')
    user2_token = user2_login['token']

    test_message = "Yippie-Kai-Yay, Motherf*****r!"
    with pytest.raises(AccessError) as e:
        message_send(user2_token, channel_1, test_message)