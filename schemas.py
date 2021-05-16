user_insert_schema = {
    'type': 'object',
    'required': ['email', 'name', 'list_nom_qr', 'pwd'],
    'properties': {
        'email': {
            'type': 'string'
        },
        'name': {
            'type': 'string'
        },
        'list_nom_qr': {
            'type': 'array'
        },
        'pwd': {
            'type': 'string'
        },
        'profile_picture': {
            'type': 'string'
        }
    },
    'additionalProperties': False
}
