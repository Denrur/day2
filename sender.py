import requests
from authentification import auth
import re

'''
Реализованы фичи-
Авторизация вынесена в отдельный модуль
Отсылка личных сообщений одному или нескольким пользователям
'''


def send_message(server_):
    print("Введите сообщение:")
    text = input()
    pattern_user = r"@([\w]+)"
    pattern_action = r'\/(reply) (\d+) (.+)'
    tag = re.findall(pattern_user, text)
    result = re.findall(pattern_action, text)
    action = 'send'
    msg_id = None
    print(result)
    if result:
        print(result)
        action, msg_id, text = result[0]
        print(text)
    if text.lower() == 'exit':
        requests.post(
            f"{server_}/send",
            json={"username": username,
                  "password": password,
                  "text": f'Всем пока \n (user {username} log out)',
                  'tag': tag}
        )
        requests.post(
            f"{server_}/auth",
            json={"username": username, "password": password, "status": "exit"}
        )
        exit()

    requests.post(
        f"{server_}/send",
        json={"username": username, "password": password, "text": text, 'tag': tag,
              'action': action, 'msg_id': msg_id}
    )

    print()


if __name__ == '__main__':
    SERVER = 'http://127.0.0.1:5000'
    try:
        response = requests.get(f"{SERVER}/status")
        print(response.text)
    except requests.exceptions.ConnectionError:
        print('Server is down')
        exit()

    username, password = auth(SERVER)

    while True:
        send_message(SERVER)

