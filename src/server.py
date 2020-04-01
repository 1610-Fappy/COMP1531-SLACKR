import sys
from json import dumps
from flask import Flask, request, abort
from flask_cors import CORS
from error import InputError
from auth import auth_register, auth_login, auth_logout

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
    
    if not request.form.get('email') or not request.form.get('password') or not request.form.get('name_first') or not request.form.get('name_last'):
        raise InputError(description='Invalid input')


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
    if register_return == "invalid name_length":
        raise InputError(description='Names must contain 1 to 50 characters') 

    return dumps(register_return)

''' =================== LOGIN A USER =================== '''
@APP.route("/auth/login", methods=['POST'])
def login():

    if not request.form.get('email') or not request.form.get('password'):
        raise InputError(description='Invalid input')

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

if __name__ == "__main__":
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080), debug=True)
