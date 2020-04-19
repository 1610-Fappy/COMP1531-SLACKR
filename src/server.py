import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from flask_mail import Mail, Message
from error import InputError, AccessError
from auth import auth_register, auth_login, auth_logout
from user import user_profile, user_setname, user_setemail, user_sethandle, user_all
from channels import channel_create, channel_invite, channel_join
from channels import channel_details, channel_listall, channel_list
from channels import channel_addowner, channel_removeowner, channel_leave
from messages import message_send, message_sendlater, message_react, message_unreact
from messages import message_pin, message_unpin, message_remove, message_edit
from messages import channel_messages
from standup import standup_start, standup_active, standup_send
from workplace import change_permission, remove_user, reset_workplace
from password import password_request, password_reset
from search import query_search

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)

mail = Mail(APP)

CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)
APP.config.update

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

''' =================== REGISTER A USER =================== '''
@APP.route("/auth/register", methods=['POST'])
def register():

    payload = request.get_json()

    if not payload:
        raise InputError(description='No args passed')
    if not 'email' in payload:
        raise InputError(description='No email passed')
    if not 'password' in payload:
        raise InputError(description='No password passed')
    if not 'name_first' in payload:
        raise InputError(description='No name_first passed')
    if not 'name_last' in payload:
        raise InputError(description='No name_last passed')

    email = payload['email']
    password = payload['password']
    name_first = payload['name_first']
    name_last = payload['name_last']

    register_return = auth_register(email, password, name_first, name_last)

    if register_return == "invalid email":
        raise InputError(description='Invalid email')
    if register_return == "used email":
        raise InputError(description='Email is already used')
    if register_return == "invalid password":
        raise InputError(description='Password must be greater than 6 characters, containing at least 1 letter and 1 number')
    if register_return == "invalid first name":
        raise InputError(description='First name must be 1 to 50 characters') 
    if register_return == "invalid last name":
        raise InputError(description='Last name must be 1 to 50 characters') 

    return dumps(register_return)

''' =================== LOGIN A USER =================== '''
@APP.route("/auth/login", methods=['POST'])
def login():

    payload = request.get_json()

    if not payload:
        raise InputError(description='No args passed')
    if not 'email' in payload:
        raise InputError(description='No email passed')
    if not 'password' in payload:
        raise InputError(description='No password passed')

    email = payload['email']
    password = payload['password']

    login_return = auth_login(email, password)

    if login_return == "invalid email":
        raise InputError(description='Invalid email')
    if login_return == "unused email":
        raise InputError(description='Email not found in records')
    if login_return == "invalid password":
        raise InputError(description='Incorrect password')

    return dumps(login_return)

''' =================== LOGS OUT A USER =================== '''
@APP.route("/auth/logout", methods=['POST'])
def logout():

    payload = request.get_json()

    if not payload or not 'token' in payload:
        raise InputError(description='No token passed')

    token = payload['token']

    logout_return = auth_logout(token)

    return dumps(logout_return)

''' =================== VIEW USER PROFILE =================== '''
@APP.route("/user/profile", methods=['GET'])
def usr_prfile():
    
    if not request.args.get('token'):
        raise InputError(description='No token passed')
    if not request.args.get('u_id'):
        raise InputError(description='No u_id passed')

    token = request.args.get('token')
    u_id = request.args.get('u_id')

    u_id = int(u_id)

    user_profile_return = user_profile(token, u_id)

    if user_profile_return == "invalid u_id":
        raise InputError(description='USER ID not found in records')
    if user_profile_return == "invalid token":
        raise InputError(description='Invalid token key')

    return dumps({
        'user': user_profile_return
    })

''' =================== CHANGE USER FIRST AND LAST NAME =================== '''
@APP.route("/user/profile/setname", methods=['PUT'])
def user_profile_setname():
    payload = request.get_json()

    if not payload:
        raise InputError(description='No args passed')
    if not 'token' in payload:
        raise InputError(description='No token passed')
    if not 'name_first' in payload:
        raise InputError(description='No first name passed')
    if not 'name_last' in payload:
        raise InputError(description='No last name passed')

    token = payload['token']
    name_first = payload['name_first']
    name_last = payload['name_last']

    user_setname_return = user_setname(token, name_first, name_last)

    if user_setname_return == "invalid first name":
        raise InputError(description="First name must be 1 to 50 characters")
    if user_setname_return == "invalid last name":
        raise InputError(description="Last name must be 1 to 50 characters")
    if user_setname_return == "invalid token":
        raise InputError(description="Invalid token key")

    return {}

''' =================== CHANGE USER EMAIL =================== '''
@APP.route("/user/profile/setemail", methods=['PUT'])
def user_profile_setemail():
    payload = request.get_json()

    if not payload:
        raise InputError(description='No args passed')
    if not 'token' in payload:
        raise InputError(description='No token passed')
    if not 'email' in payload:
        raise InputError(description='No email passed')

    token = payload['token']
    email = payload['email']

    user_setemail_return = user_setemail(token, email)

    if user_setemail_return == "invalid token":
        raise InputError(description="Invalid token key")
    if user_setemail_return == "invalid email":
        raise InputError(description="Invalid email")
    if user_setemail_return == "email used":
        raise InputError(description="Email is already used")

    return {}

''' =================== CHANGE USER HANDLE =================== '''
@APP.route("/user/profile/sethandle", methods=['PUT'])
def user_profile_sethandle():
    payload = request.get_json()

    if not payload:
        raise InputError(description='No args passed')
    if not 'token' in payload:
        raise InputError(description='No token passed')
    if not 'handle_str' in payload:
        raise InputError(description='No handle_str passed')

    token = payload['token']
    handle_str = payload['handle_str']

    user_sethandle_return = user_sethandle(token, handle_str)

    if user_sethandle_return == "invalid token":
        raise InputError(description="Invalid token key")
    if user_sethandle_return == "invalid username":
        raise InputError(description="Username must be 2 to 20 characters")
    if user_sethandle_return == "used username":
        raise InputError(description="Username already taken")

    return {}

''' =================== VIEW ALL USERS =================== '''
@APP.route("/users/all", methods=['GET'])
def users_all():
  
    if not request.args.get('token'):
        raise InputError(description='No token passed')

    token = request.args.get('token')

    user_all_return = user_all(token)

    if user_all_return == "invalid token":
        raise InputError(description="Invalid token key")

    return dumps(
        {
        "users": user_all_return
        }
    )

''' =================== CREATE CHANNEL =================== '''
@APP.route("/channels/create", methods=['POST'])
def channels_create():
    payload = request.get_json()

    if not payload:
        raise InputError(description='No args passed')
    if not 'token' in payload:
        raise InputError(description='No token passed')
    if not 'name' in payload:
        raise InputError(description='No name passed')
    if not 'is_public' in payload:
        raise InputError(description='No is_public passed')

    token = payload['token']
    name = payload['name']
    is_public = payload['is_public']

    channels_create_return = channel_create(token, name, is_public)

    if channels_create_return == "invalid token":
        raise InputError(description='Invalid token key')
    if channels_create_return == 'invalid channel name_length':
        raise InputError(description='Channel name cannot be more than 20 characters')

    return dumps(channels_create_return)

''' =================== INVITE TO CHANNEL =================== '''
@APP.route("/channel/invite", methods=['POST'])
def channels_invite():
    payload = request.get_json()

    if not payload:
        raise InputError(description='No args passed')
    if not 'token' in payload:
        raise InputError(description='No token passed')
    if not 'channel_id' in payload:
        raise InputError(description='No channel_id passed')
    if not 'u_id' in payload:
        raise InputError(description='No u_id passed')

    token = payload['token']
    channel_id = payload['channel_id']
    u_id = payload['u_id']

    u_id = int(u_id)
    channel_id = int(channel_id)

    channel_invite_return = channel_invite(token, channel_id, u_id)

    if channel_invite_return == "invalid token":
        raise InputError(description='Invalid token key')
    if channel_invite_return == "invalid channel_id":
        raise InputError(description="Channel_id does not match authorised user's request")
    if channel_invite_return == "invalid u_id":
        raise InputError(description="Invited user does not exist")
    if channel_invite_return == "already member":
        raise InputError(description="Invited user is already a member")
    if channel_invite_return == "not member":
        raise AccessError(description="Authorised user is not part of the channel")
    

    return {}

''' =================== JOIN A CHANNEL =================== '''
@APP.route("/channel/join", methods=['POST'])
def channels_join():
    payload = request.get_json()

    if not payload:
        raise InputError(description='No args passed')
    if not 'token' in payload:
        raise InputError(description='No token passed')
    if not 'channel_id' in payload:
        raise InputError(description='No channel_id passed')

    token = payload['token']
    channel_id = payload['channel_id']
    channel_id = int(channel_id)

    channel_join_return = channel_join(token, channel_id)

    if channel_join_return == "invalid token":
        raise InputError(description='Invalid token key')
    if channel_join_return == "invalid channel_id":
        raise InputError(description="Invalid Channel ID")
    if channel_join_return == "not public":
        raise AccessError(description='Trying to join private channel without authorisation')
    

    return {}

''' =================== SHOW CHANNEL DETAILS =================== '''
@APP.route("/channel/details", methods=['GET'])
def channels_details():

    if not request.args.get('token'):
        raise InputError(description='No token passed')
    if not request.args.get('channel_id'):
        raise InputError(description='No channel_id passed')

    token = request.args.get('token')
    channel_id = request.args.get('channel_id')

    channel_id = int(channel_id)

    channel_details_return = channel_details(token, channel_id)

    if channel_details_return == "invalid token":
        raise InputError(description='Invalid token key')
    if channel_details_return == "invalid channel_id":
        raise InputError(description="Invalid Channel ID")
    if channel_details_return == "not member":
        raise AccessError(description="Authorised user is not part of the channel")

    return dumps(channel_details_return)

''' =================== SHOW ALL CHANNELS =================== '''
@APP.route("/channels/listall", methods=['GET'])
def channels_listall():

    if not request.args.get('token'):
        raise InputError(description='No token passed')

    token = request.args.get('token')

    channel_listall_return = channel_listall(token)

    if channel_listall_return == "invalid token":
        raise InputError(description='Invalid token key')  

    return dumps(channel_listall_return)

''' =================== SHOW CHANNELS USER IS IN =================== '''
@APP.route("/channels/list", methods=['GET'])
def channels_list():

    if not request.args.get('token'):
        raise InputError(description='No token passed')

    token = request.args.get('token')

    channel_list_return = channel_list(token)

    if channel_list_return == "invalid token":
        raise InputError(description='Invalid token key')  

    return dumps(channel_list_return)

''' =================== MAKE MEMBER OWNER  =================== '''
@APP.route("/channel/addowner", methods=['POST'])
def channels_addowner():
    payload = request.get_json()

    if not payload:
        raise InputError(description='No args passed')
    if not 'token' in payload:
        raise InputError(description='No token passed')
    if not 'channel_id' in payload:
        raise InputError(description='No channel_id passed')
    if not 'u_id' in payload:
        raise InputError(description='No u_id passed')

    token = payload['token']
    channel_id = payload['channel_id']
    u_id = payload['u_id']

    u_id = int(u_id)
    channel_id = int(channel_id)

    channel_addowner_return = channel_addowner(token, channel_id, u_id)

    if channel_addowner_return == "invalid token":
        raise InputError(description='Invalid token key')  
    if channel_addowner_return == "invalid channel_id":
        raise InputError(description="Invalid Channel ID")
    if channel_addowner_return == "not owner":
        raise AccessError(description="Authorised user is not an owner")
    if channel_addowner_return == "already owner":
        raise AccessError(description="User is already an owner")

    return {}

''' =================== REMOVE OWNER STATUS FROM MEMBER  =================== '''
@APP.route("/channel/removeowner", methods=['POST'])
def channels_removeowner():
    payload = request.get_json()

    if not payload:
        raise InputError(description='No args passed')
    if not 'token' in payload:
        raise InputError(description='No token passed')
    if not 'channel_id' in payload:
        raise InputError(description='No channel_id passed')
    if not 'u_id' in payload:
        raise InputError(description='No u_id passed')

    token = payload['token']
    channel_id = payload['channel_id']
    u_id = payload['u_id']

    u_id = int(u_id)
    channel_id = int(channel_id)

    channel_removeowner_return = channel_removeowner(token, channel_id, u_id)

    if channel_removeowner_return == "invalid token":
        raise InputError(description='Invalid token key')  
    if channel_removeowner_return == "invalid channel_id":
        raise InputError(description="Invalid Channel ID")
    if channel_removeowner_return == "token user not owner":
        raise AccessError(description="Authorised user is not an owner")
    if channel_removeowner_return == "not owner":
        raise AccessError(description="User is not an owner")

    return {}

''' =================== REMOVE OWNER STATUS FROM MEMBER  =================== '''
@APP.route("/channel/leave", methods=['POST'])
def leave_channel():
    payload = request.get_json()

    if not payload:
        raise InputError(description='No args passed')
    if not 'token' in payload:
        raise InputError(description='No token passed')
    if not 'channel_id' in payload:
        raise InputError(description='No channel_id passed')

    token = payload['token']
    channel_id = payload['channel_id']

    channel_id = int(channel_id)

    channel_leave_return = channel_leave(token, channel_id)

    if channel_leave_return == "invalid token":
        raise InputError(description='Invalid token key')
    if channel_leave_return == "invalid channel_id":
        raise InputError(description="Invalid Channel ID")
    if channel_leave_return == "not member":
        raise AccessError(description="Authorised user is not part of the channel")    

    return {}


''' =================== SEND A MESSAGE IN A CHANNEL  =================== '''
@APP.route("/message/send", methods=['POST'])
def msg_send():
    payload = request.get_json()

    if not payload:
        raise InputError(description='No args passed')
    if not 'token' in payload:
        raise InputError(description='No token passed')
    if not 'channel_id' in payload:
        raise InputError(description='No channel_id passed')
    if not 'message' in payload:
        raise InputError(description='No message passed')

    token = payload['token']
    channel_id = payload['channel_id']
    message = payload['message']

    channel_id = int(channel_id)

    message_send_return = message_send(token, channel_id, message)

    if message_send_return == "invalid token":
        raise InputError(description='Invalid token key')
    if message_send_return == "invalid channel_id":
        raise InputError(description="Invalid Channel ID")
    if message_send_return == "more than 1000 characters":
        raise InputError(description="Message must be less than 1000 characters")
    if message_send_return == "not member":
        raise AccessError(description="User is not a member of this channel")

    return dumps({
        'message_id': message_send_return
    })

''' ================ SEND A MESSAGE LATER IN A CHANNEL  ================ '''
@APP.route("/message/sendlater", methods=['POST'])
def msg_sendlater():
    payload = request.get_json()

    if not payload:
        raise InputError(description='No args passed')
    if not 'token' in payload:
        raise InputError(description='No token passed')
    if not 'channel_id' in payload:
        raise InputError(description='No channel_id passed')
    if not 'message' in payload:
        raise InputError(description='No message passed')
    if not 'time_sent' in payload:
        raise InputError(description='No time_sent passed')

    token = payload['token']
    channel_id = payload['channel_id']
    message = payload['message']
    time_sent = payload['time_sent']

    channel_id = int(channel_id)
    time_sent = int(time_sent)

    message_sendlater_return = message_sendlater(token, channel_id, message, time_sent)

    if message_sendlater_return == "invalid token":
        raise InputError(description='Invalid token key')
    if message_sendlater_return == "invalid channel_id":
        raise InputError(description="Invalid Channel ID")
    if message_sendlater_return == "more than 1000 characters":
        raise InputError(description="Message must be less than 1000 characters")
    if message_sendlater_return == "time passed":
        raise InputError(description="Cannot send messages in the past")
    if message_sendlater_return == "not member":
        raise AccessError(description="User is not a member of this channel")

    return dumps({
        'message_id': message_sendlater_return
    })

''' ================ REACT TO A MESSAGE IN A CHANNEL  ================ '''
@APP.route("/message/react", methods=['POST'])
def msg_react():
    payload = request.get_json()

    if not payload:
        raise InputError(description='No args passed')
    if not 'token' in payload:
        raise InputError(description='No token passed')
    if not 'message_id' in payload:
        raise InputError(description='No message_id passed')
    if not 'react_id' in payload:
        raise InputError(description='No react_id passed')

    token = payload['token']
    message_id = payload['message_id']
    react_id = payload['react_id']

    message_id = int(message_id)
    react_id = int(react_id)

    message_react_return = message_react(token, message_id, react_id)

    if message_react_return == "invalid token":
        raise InputError(description='Invalid token key')
    if message_react_return == "invalid message_id":
        raise InputError(description="Invalid Message ID")
    if message_react_return == "invalid react_id":
        raise InputError(description="Invalid React ID")
    # if message_react_return == "already reacted to":
    #     raise InputError(description="Already reacted")
    if message_react_return == "not a member":
        raise AccessError(description="Not a member of channel")

    return dumps({})

''' ================ REACT TO A MESSAGE IN A CHANNEL  ================ '''
@APP.route("/message/unreact", methods=['POST'])
def msg_unreact():
    payload = request.get_json()

    if not payload:
        raise InputError(description='No args passed')
    if not 'token' in payload:
        raise InputError(description='No token passed')
    if not 'message_id' in payload:
        raise InputError(description='No message_id passed')
    if not 'react_id' in payload:
        raise InputError(description='No react_id passed')

    token = payload['token']
    message_id = payload['message_id']
    react_id = payload['react_id']

    message_id = int(message_id)
    react_id = int(react_id)

    message_unreact_return = message_unreact(token, message_id, react_id)

    if message_unreact_return == "invalid token":
        raise InputError(description='Invalid token key')
    if message_unreact_return == "invalid message_id":
        raise InputError(description="Invalid Message ID")
    if message_unreact_return == "invalid react_id":
        raise InputError(description="Invalid React ID")
    if message_unreact_return == "not a member":
        raise AccessError(description="Not a member of channel")

    return dumps({})

''' ================ PIN A MESSAGE IN A CHANNEL  ================ '''
@APP.route("/message/pin", methods=['POST'])
def msg_pin():
    payload = request.get_json()

    if not payload:
        raise InputError(description='No args passed')
    if not 'token' in payload:
        raise InputError(description='No token passed')
    if not 'message_id' in payload:
        raise InputError(description='No message_id passed')

    token = payload['token']
    message_id = payload['message_id']

    message_id = int(message_id)

    message_pin_return = message_pin(token, message_id)

    if message_pin_return == "invalid token":
        raise InputError(description='Invalid token key')
    if message_pin_return == "invalid message_id":
        raise InputError(description="Invalid Message ID")
    if message_pin_return == "already pinned":
        raise InputError(description="Message already pinned")
    if message_pin_return == "not member":
        raise AccessError(description="Authorised user is not a member of this channel")
    if message_pin_return == "not owner":
        raise AccessError(description="Authorised user is not an owner of this channel")

    return dumps({})

''' ================ UNPIN A MESSAGE IN A CHANNEL  ================ '''
@APP.route("/message/unpin", methods=['POST'])
def msg_unpin():
    payload = request.get_json()

    if not payload:
        raise InputError(description='No args passed')
    if not 'token' in payload:
        raise InputError(description='No token passed')
    if not 'message_id' in payload:
        raise InputError(description='No message_id passed')

    token = payload['token']
    message_id = payload['message_id']

    message_id = int(message_id)

    message_unpin_return = message_unpin(token, message_id)

    if message_unpin_return == "invalid token":
        raise InputError(description='Invalid token key')
    if message_unpin_return == "invalid message_id":
        raise InputError(description="Invalid Message ID")
    if message_unpin_return == "already unpinned":
        raise InputError(description="Message already unpinned")
    if message_unpin_return == "not member":
        raise AccessError(description="Authorised user is not a member of this channel")
    if message_unpin_return == "not owner":
        raise AccessError(description="Authorised user is not an owner of this channel")

    return dumps({})

''' ================ REMOVE A MESSAGE IN A CHANNEL  ================ '''
@APP.route("/message/remove", methods=['DELETE'])
def msg_remove():
    payload = request.get_json()

    if not payload:
        raise InputError(description='No args passed')
    if not 'token' in payload:
        raise InputError(description='No token passed')
    if not 'message_id' in payload:
        raise InputError(description='No message_id passed')

    token = payload['token']
    message_id = payload['message_id']

    message_id = int(message_id)

    message_remove_return = message_remove(token, message_id)

    if message_remove_return == "invalid token":
        raise InputError(description='Invalid token key')
    if message_remove_return == "invalid message_id":
        raise InputError(description="Invalid Message ID")
    if message_remove_return == "not member":
        raise AccessError(description="Authorised user is not a member of this channel")
    if message_remove_return == "not owner":
        raise AccessError(description="Authorised user is not an owner of this channel")

    return dumps({})

''' ================ EDIT A MESSAGE IN A CHANNEL  ================ '''
@APP.route("/message/edit", methods=['PUT'])
def msg_edit():
    payload = request.get_json()

    if not payload:
        raise InputError(description='No args passed')
    if not 'token' in payload:
        raise InputError(description='No token passed')
    if not 'message_id' in payload:
        raise InputError(description='No message_id passed')
    if not 'message' in payload:
        raise InputError(description='No message passed')

    token = payload['token']
    message_id = payload['message_id']
    message = payload['message']

    message_id = int(message_id)

    message_edit_return = message_edit(token, message_id, message)

    if message_edit_return == "invalid token":
        raise InputError(description='Invalid token key')
    if message_edit_return == "more than 1000 characters":
        raise InputError(description="Message must be less than 1000 characters")
    if message_edit_return == "invalid message_id":
        raise InputError(description="Invalid Message ID")
    if message_edit_return == "not member":
        raise AccessError(description="Authorised user is not a member of this channel")
    if message_edit_return == "not owner":
        raise AccessError(description="Authorised user is not an owner of this channel")

    return dumps({})

''' ================ LOAD MESSAGEs IN A CHANNEL  ================ '''
@APP.route("/channel/messages", methods=['GET'])
def load_messages():
    
    if not request.args.get('token'):
        raise InputError(description='No token passed')
    if not request.args.get('channel_id'):
        raise InputError(description='No channel_id passed')
    if not request.args.get('start'):
        raise InputError(description='No start passed')

    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    start = request.args.get('start')

    start = int(start)
    channel_id = int(channel_id)

    channel_messages_return = channel_messages(token, channel_id, start)

    if channel_messages_return == "invalid token":
        raise InputError(description='Invalid token key')
    if channel_messages_return == "invalid channel_id":
        raise InputError(description="Invalid Channel ID")
    if channel_messages_return == "not member":
        raise AccessError(description="Authorised user is not a member of this channel")
    
    return dumps(channel_messages_return)

''' =================== STARTS A STARTUP  =================== '''
@APP.route("/standup/start", methods=['POST'])
def start_standup():
    payload = request.get_json()

    if not payload:
        raise InputError(description='No args passed')
    if not 'token' in payload:
        raise InputError(description='No token passed')
    if not 'channel_id' in payload:
        raise InputError(description='No channel_id passed')
    if not 'length' in payload:
        raise InputError(description='No length of time passed')

    token = payload['token']
    channel_id = int(payload['channel_id'])
    length = int(payload['length'])

    standup_start_return = standup_start(token, channel_id, length)

    if standup_start_return == "invalid token":
        raise InputError(description='Invalid token key')  
    if standup_start_return == "invalid channel_id":
        raise InputError(description="Invalid Channel ID")
    if standup_start_return == "standup already active":
        raise AccessError(description="Standup is already in Progress")

    return dumps(standup_start_return)

''' =================== CHECKS IS STANDUP IS ACTIVE =================== '''
@APP.route("/standup/active", methods=['GET'])
def active_standup():
    
    if not request.args.get('token'):
        raise InputError(description='No token passed')
    if not request.args.get('channel_id'):
        raise InputError(description='No channel_id passed')

    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))

    standup_active_return = standup_active(token, channel_id)

    if standup_active_return == "invalid token":
        raise InputError(description='Invalid token key')  
    if standup_active_return == "invalid channel_id":
        raise InputError(description="Invalid Channel ID")

    return dumps(standup_active_return)

''' =================== SENDS A MESSAGE TO STANDUP =================== '''
@APP.route("/standup/send", methods=['POST'])
def send_startup_msg():
    payload = request.get_json()

    if not payload:
        raise InputError(description='No args passed')
    if not 'token' in payload:
        raise InputError(description='No token passed')
    if not 'channel_id' in payload:
        raise InputError(description='No channel_id passed')
    if not 'message' in payload:
        raise InputError(description='No message passed')

    token = payload['token']
    channel_id = int(payload['channel_id'])
    message = payload['message']

    standup_send_return = standup_send(token, channel_id, message)

    if standup_send_return == "invalid token":
        raise InputError(description='Invalid token key')  
    if standup_send_return == "invalid channel_id":
        raise InputError(description="Invalid Channel ID")
    if standup_send_return == "More than 1000 characters":
        raise InputError(description="Message is too long")
    if standup_send_return == "not member":
        raise AccessError(description="Authorised user is not part of the channel")

    return {}

''' =================== CHANGES A USER'S PERMISSION  =================== '''
@APP.route("/admin/userpermission/change", methods=['POST'])
def change_permissions():
    payload = request.get_json()

    if not payload:
        raise InputError(description='No args passed')
    if not 'token' in payload:
        raise InputError(description='No token passed')
    if not 'u_id' in payload:
        raise InputError(description='No u_id passed')
    if not 'permission_id' in payload:
        raise InputError(description='No permission_id passed')

    token = payload['token']
    u_id = int(payload['u_id'])
    permission_id = int(payload['permission_id'])

    change_permission_return = change_permission(token, u_id, permission_id)

    if change_permission_return == "invalid token":
        raise InputError(description='Invalid token key')  
    if change_permission_return == "invalid permission_id":
        raise InputError(description="Invalid Permission ID")
    if change_permission_return == "invalid permissions":
        raise AccessError(description="User is not Authorised")
    if change_permission_return == "invalid u_id":
        raise AccessError(description="User ID is invalid")

    return {}

''' =================== REMOVES A USER FROM SLACK =================== '''
@APP.route("/admin/user/remove", methods=['DELETE'])
def remove_users():
    payload = request.get_json()

    if not payload:
        raise InputError(description='No args passed')
    if not 'token' in payload:
        raise InputError(description='No token passed')
    if not 'u_id' in payload:
        raise InputError(description='No u_id passed')

    token = payload['token']
    u_id = int(payload['u_id'])

    remove_user_return = remove_user(token, u_id)

    if remove_user_return == "invalid token":
        raise InputError(description='Invalid token key')  
    if remove_user_return == "invalid permissions":
        raise AccessError(description="User is not Authorised")
    if remove_user_return == "invalid u_id":
        raise AccessError(description="User ID is invalid")

    return {}

''' =================== RESETS WORKSPACE =================== '''
@APP.route("/workspace/reset", methods=['POST'])
def refresh():
    reset_workplace()
    return {}

''' =================== RESET PASSWORD REQUEST =================== '''
@APP.route("/auth/passwordreset/request", methods=['POST'])
def request_code():
    payload = request.get_json()

    if not payload:
        raise InputError(description='No args passed')
    if not 'email' in payload:
        raise InputError(description='No Email passed')

    email = payload['email']

    request_code_return = password_request(email)

    if request_code_return == "not a user":
        raise InputError(description='The requested email does not belong to a user') 


    msg = Message("Password Reset Request", sender="SLACKRSERVER@gmail.com", recipients=[email])
    code = "Your Password Reset Code is:\n" + request_code_return
    msg.body = code
    mail.send(msg)

    return {}

''' =================== RESET PASSWORD GIVEN RESET CODE  =================== '''
@APP.route("/auth/passwordreset/reset", methods=['POST'])
def reset_password():
    payload = request.get_json()

    if not payload:
        raise InputError(description='No args passed')
    if not 'reset_code' in payload:
        raise InputError(description='No Reset Code passed')
    if not 'new_password' in payload:
        raise InputError(description='No new Password to be set')

    reset_code = payload['reset_code']
    new_password = payload['new_password']

    reset_pass_return = password_reset(reset_code, new_password)

    if reset_pass_return == "invalid password":
        raise InputError(description='The inputed password is not valid')
    if reset_pass_return == "invalid reset code":
        raise InputError(description='The inputted code is invalid')  

    return {}

''' =================== SEARCH  =================== '''
@APP.route("/search", methods=['GET'])
def search_string():
    
    if not request.args.get('token'):
        raise InputError(description='No Token passed')
    if not request.args.get('query_str'):
        raise InputError(description='No Query String passed')

    token = request.args.get('token')
    query_str = request.args.get('query_str')

    search_return = query_search(token, query_str)

    if search_return == "invalid token":
        raise InputError(description='Invalid token key')

    return dumps(search_return)



if __name__ == "__main__":
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080), debug=True)
