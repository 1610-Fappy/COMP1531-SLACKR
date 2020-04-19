import sys
from json import dumps
from flask import Flask, request, abort
from flask_cors import CORS
from flask_mail import Mail, Message
from error import InputError, AccessError
from auth import auth_register, auth_login, auth_logout
from user import user_profile, user_setname, user_setemail, user_sethandle, user_all
from channels import channel_create, channel_invite, channel_join
from channels import channel_details, channel_listall, channel_list
from channels import channel_addowner, channel_removeowner, channel_leave
from workplace import change_permission, remove_user, reset_workplace
from standup import standup_start, standup_active, standup_send
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
CORS(APP)
mail = Mail(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.config(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME = 'SLACKRSERVER@gmail.com',
    MAIL_PASSWORD = 'Password123'
)
APP.register_error_handler(Exception, defaultHandler)

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

    user_profile_return = user_profile(token, u_id)

    if user_profile_return == "invalid u_id":
        raise InputError(description='USER ID not found in records')
    if user_profile_return == "invalid token":
        raise InputError(description='Invalid token key')

    print(user_profile_return)

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

    return (
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

    channel_join_return = channel_join(token, channel_id)

    if channel_join_return == "invalid token":
        raise InputError(description='Invalid token key')
    if channel_join_return == "invalid channel_id":
        raise InputError(description="Invalid Channel ID")
    if channel_join_return == "not public":
        raise AccessError(description='Trying to join private channel without authorisation')
    

    return {}

''' =================== LEAVE A CHANNEL ======================== '''
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

    channel_leave_return = channel_leave(token, channel_id)

    if channel_leave_return == "invalid token":
        raise InputError(description='Invalid token key')
    if channel_leave_return == "invalid channel_id":
        raise InputError(description="Invalid Channel ID")
    if channel_leave_return == "not member":
        raise AccessError(description="Authorised user is not part of the channel")    

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


''' =================== Starts a Standup  =================== '''
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

''' =================== Checks if Standup is Active =================== '''
@APP.route("/standup/active", methods=['GET'])
def active_standup():
    payload = request.get_json()

    if not payload:
        raise InputError(description='No args passed')
    if not 'token' in payload:
        raise InputError(description='No token passed')
    if not 'channel_id' in payload:
        raise InputError(description='No channel_id passed')

    token = payload['token']
    channel_id = int(payload['channel_id'])

    standup_active_return = standup_active(token, channel_id)

    if standup_active_return == "invalid token":
        raise InputError(description='Invalid token key')  
    if standup_active_return == "invalid channel_id":
        raise InputError(description="Invalid Channel ID")

    return dumps(standup_active_return)

''' =================== Sends message to Standup =================== '''
@APP.route("/standup/active", methods=['POST'])
def active_standup():
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


''' =================== Change permissions for user  =================== '''
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

''' =================== Request to send code to reset password  =================== '''
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
    else:
        msg = Message("Password Reset Request", sender="SLACKRSERVER@gmail.com", recipients=[email])
        msg.body = "Your Password Reset Code is:\n" + request_code_return
        mail.send(msg)
    return {}

''' =================== Request to send code to reset password  =================== '''
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
    else:
        msg = Message("Password Reset Request", sender="SLACKRSERVER@gmail.com", recipients=[email])
        msg.body = "Your Password Reset Code is:\n" + request_code_return
        mail.send(msg)
    return {}

''' =================== Reset password given reset code  =================== '''
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
        raise InputError(description='The inputted password is not valid')
    if reset_pass_return == "invalid reset code":
        raise InputError(description='The inputted code is invalid')  

    return {}

''' =================== Searches for query string  =================== '''
@APP.route("/auth/passwordreset/reset", methods=['GET'])
def search_string():
    payload = request.get_json()

    if not payload:
        raise InputError(description='No args passed')
    if not 'token' in payload:
        raise InputError(description='No Token passed')
    if not 'query_str' in payload:
        raise InputError(description='No Query String passed')

    token = payload['token']
    query_str = payload['query_str']

    search_return = query_search(token, query_str)

    if search_return == "invalid token":
        raise InputError(description='Invalid token key')

    return dumps(search_return)

''' =================== Remove user from slackr =================== '''
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

''' =================== Clears Workplace =================== '''
@APP.route("/workspace/reset", methods=['POST'])
def refresh():
    reset_workplace()
    return {}

if __name__ == "__main__":
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080), debug=True)

# FIX
# - changing request?
