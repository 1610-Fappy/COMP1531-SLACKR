import pickle

DATA_STRUCTURE = {
    'channel': [
        {
            'name': ''
        }
    ]
    'user': [
        {
            
        }
    ]
}

with open('database.p', 'wb') as FILE:
    pickle.dump(DATA_STRUCTURE, FILE)
