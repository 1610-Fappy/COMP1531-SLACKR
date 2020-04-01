import sys
from json import dumps
from flask import Flask, request, abort
from flask_cors import CORS
from error import InputError
from auth import auth_register, auth_login, auth_logout
from user import user_profile, user_setname, user_setemail, user_sethandle, user_all

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

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
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
    
    if not request.form.get('email'):
        raise InputError(description='Email not entered')
    if not request.form.get('password'):
        raise InputError(description='Password not entered')
    if not request.form.get('name_first'):
        raise InputError(description='First name not entered')
    if not request.form.get('name_last'):
        raise InputError(description='Last name not entered')

    email = request.form.get('email')
    password = request.form.get('password')
    name_first = request.form.get('name_first')
    name_last = request.form.get('name_last')

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

    if not request.form.get('email'):
        raise InputError(description='Email not entered')
    if not request.form.get('password'):
        raise InputError(description='Password not entered')

    email = request.form.get('email')
    password = request.form.get('password')

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
    
    payload = request.get_json()

    if not payload:
        raise InputError(description='No args passed')
    if not 'token' in payload:
        raise InputError(description='No token passed')
    if not 'u_id' in payload:
        raise InputError(description='No u_id passed')

    token = payload['token']
    u_id = payload['u_id']

    user_profile_return = user_profile(token, u_id)

    if user_profile_return == "invalid u_id":
        raise InputError(description='USER ID not found in records')
    if user_profile_return == "invalid token":
        raise InputError(description='Invalid token key')

    return dumps(user_profile_return)

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

''' =================== CHANGE USER HANDLE =================== '''
@APP.route("/users/all", methods=['GET'])
def users_all():
    payload = request.get_json()

    if not payload:
        raise InputError(description='No args passed')
    if not 'token' in payload:
        raise InputError(description='No token passed')

    token = payload['token']

    user_all_return = user_all(token)

    if user_all_return == "invalid token":
        raise InputError(description="Invalid token key")

    return (
        {
        "USERS": user_all_return
        }
    )

if __name__ == "__main__":
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080), debug=True)


