''' File to store data'''

DATA = {
    'users' : [],
    'active_tokens' : []
}

def get_data():
    ''' Access global data from one point'''
    global DATA
    return DATA
