import time
from datetime import datetime
from authentification import auth
import requests


def get_messages(user, server_, last=None):
    resp = requests.get(f"{server_}/messages",
                        params={'after': last, 'user': user})
    messages = resp.json()["messages"]

    for message in messages:
        beauty_time = datetime.fromtimestamp(message["time"])
        beauty_time = beauty_time.strftime('%d/%m/%Y %H:%M:%S')
        print(message["username"], beauty_time)
        print(message['id'], message["text"], '\n')

        last = message["time"]

    time.sleep(1)
    return last


if __name__ == '__main__':
    last_time = 0
    server = 'http://127.0.0.1:5000'
    try:
        response = requests.get(f"{server}/status")
        print(response.text)
    except requests.exceptions.ConnectionError:
        print('Server is down')
        exit()

    username, password = auth(server)

    while True:
        last_time = get_messages(username, server_=server, last=last_time)
