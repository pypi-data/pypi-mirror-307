import json

def get_json_from_figma_file():
    figma_tokens_file = open('figma_tokens.json', 'r')
    figma_dict = json.load(figma_tokens_file)

    strings_dict = {}
    for key in figma_dict['global']:
        token = figma_dict['global'][key]
        if(token['type']=='text'):
            strings_dict[key]=token['value']
    
    return json.dumps(strings_dict)

def update_figma_file_locally(json_string):
    new_strings = json.loads(json_string)
    figma_dict = dict()
    figma_dict['global'] = dict()
    for key in new_strings:
        figma_dict['global'][key] = dict()
        figma_dict['global'][key]['type'] = 'text'
        figma_dict['global'][key]['value'] = new_strings[key]

    new_json = json.dumps(figma_dict)

    with open('figma_tokens.json', 'w') as f:
        f.write(new_json)

def update_rc_locally():
    rc_file = open('config.json', 'r')
    rc_dict = json.load(rc_file)

    strings_json = get_json_from_figma_file()

    rc_dict['parameters']['strings'] = dict()
    rc_dict['parameters']['strings']['defaultValue'] = dict()
    rc_dict['parameters']['strings']['defaultValue']['value'] = strings_json
    rc_dict['parameters']['strings']['valueType'] = 'JSON'
    rc_json = json.dumps(rc_dict)

    with open('config.json', 'w') as f:
        f.write(rc_json)

def get_json_from_rc_file():
    rc_file = open('config.json', 'r')
    rc_dict = json.load(rc_file)
    return json.loads(rc_dict['parameters']['strings']['defaultValue']['value'])