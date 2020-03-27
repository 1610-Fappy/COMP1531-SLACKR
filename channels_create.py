def channels_create(token, name, is_public):
    # Assume all input is correct
    channels = {
        "token" : '',
        "name" : {},
        "is_public" : '',
    }

    channels['name'] = name
    channels['is_public'] = is_public

    return {
        "channel_id": {}
    }
