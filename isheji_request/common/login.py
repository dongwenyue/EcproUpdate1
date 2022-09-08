import requests
from common.read_yaml import url, username, password


def login():

    body = {
        'en_name': f'{username}',
        'pass': f'{password}',
    }
    resp = requests.request(method='post', url=url, json=body)
    return resp.json()


# login = login()
# print(login)
# token = login['data']['token']
# print(token)
