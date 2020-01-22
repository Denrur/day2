import getpass
import requests


def auth(server):
    username = input("Введите имя: \n")

    password = getpass.getpass("Введите пароль: \n")

    response = requests.post(
        f"{server}/auth",
        json={"username": username, "password": password, "status": "enter"}
    )
    if not response.json()['ok']:
        print('Неверный пароль')
        exit()
    return username, password
