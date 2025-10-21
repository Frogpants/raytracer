import json

def update_json(jsn_name, data):
    with open(jsn_name, 'w') as f:
        json.dump(data, f, indent=4)

def read_json(jsn_name):
    with open(jsn_name, 'r') as f:
        data = json.load(f)
    return data
