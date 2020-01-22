import os
import time
from datetime import datetime

from flask import Flask, request

import json
app = Flask(__name__)

'''
Вьюха /status дополнительно показывает общее количество сообщений,а так же количество пользователей онлайн

Реализованы фичи-
Загрузка/Сохранение истории сообщений и списка пользователей
Очистка файлов с историей сообщений и списком пользователей(/wipe)
Ответ на определенное сообщение
'''
messages = []
users = {}
path = os.path.dirname(os.path.realpath(__file__))
messages_log = os.path.join(path, 'messages.txt')
users_db = os.path.join(path, 'users.txt')

try:
    with open(messages_log, 'r') as load_history:
        messages = json.load(load_history)
except FileNotFoundError:
    print('There is no saved messages')


try:
    with open(users_db, 'r') as load_users:
        users = json.load(load_users)
except FileNotFoundError:
    print('There is no saved users')

try:
    last_id = max([message['id'] for message in messages])

except ValueError:
    last_id = 0


@app.route("/")
def hello_view():
    return "<h1>Welcome to Python messenger!</h1>"


@app.route("/status")
def status_view():
    users_online = len([user for user in users if users[user]['online']])
    total_users = len(users)
    return {
            'status': True,
            'time': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            'total_users': total_users,
            'users online': users_online,
            'total messages': len(messages)
        }


@app.route("/wipe")
def wipe_server():
    os.remove(messages_log)
    os.remove(users_db)
    return "Server wiped"


@app.route("/messages")
def messages_view():
    """
    Получение сообщений после отметки after
    input: after - отметка времени, user - пользователь запрашивающий сообщения
    output: {
        "messages": [
            {"username": str, "text": str, "time": float}, 'tag': str
            ...
        ]
    }
    """
    after = float(request.args['after'])
    user = request.args['user']
    new_messages = [message for message in messages if message['time'] > after and
                    (user in message['tag'] or not message['tag'])]
    return {'messages': new_messages}


@app.route("/send", methods=['POST'])
def send_view():
    global last_id
    """
    Отправка сообщений
    input: {
        "username": str,
        "password": str,
        "text": str,
        "status": str,
        "tag': list, 
        "action": str,
        "msg_id": int
    }
    output: {"ok": bool}
    """
    data = request.json
    username = data["username"]
    password = data["password"]

    if username not in users or users[username]['password'] != password:
        return {"ok": False}

    text = data["text"]
    tag = data['tag']
    action = data['action']
    msg_id = data.get('msg_id')

    last_id += 1

    if action == 'reply':
        text = [message for message in messages if message['id'] == int(msg_id)][0]['text'] + "\n" + text
        print(text)
    messages.append({"username": username, "text": text, "time": time.time(), 'tag': tag, 'id': last_id})
    last_id += 1
    return {'ok': True}


@app.route("/auth", methods=['POST'])
def auth_view():
    """
    Авторизовать пользователя или сообщить что пароль неверный.
    input: {
        "username": str,
        "password": str
    }
    output: {"ok": bool}
    """
    data = request.json
    username = data["username"]
    password = data["password"]
    status = data.get("status")

    if status == 'exit':
        users[username]['online'] = False
        return {"ok": True}

    if username not in users:
        users[username] = {'password': password, 'online': True}
        return {"ok": True}
    elif users[username]['password'] == password:
        users[username]['online'] = True
        return {"ok": True}
    else:
        return {"ok": False}


@app.route('/shutdown')
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    with open(messages_log, 'w') as save_history:
        json.dump(messages, save_history)
    for user in users:
        users[user]['online'] = False
    with open(users_db, 'w') as save_users:
        json.dump(users, save_users)
    func()
    return 'Server shutting down...'


if __name__ == '__main__':
    app.run()
