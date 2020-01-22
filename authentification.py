import getpass
import requests


def auth(server):
    while True:
        username = input("Введите имя: \n")

        password = getpass.getpass("Введите пароль: \n")

        response = requests.post(
            f"{server}/auth",
            json={"username": username, "password": password, "status": "enter"}
        )
        if not response.json()['ok']:
            print('Неверный пароль')
            continue
        return username, password
