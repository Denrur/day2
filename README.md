# day2
Метод /status показывает общее число сообщений а так же общее количество
зарегестрированных пользователей и количество пользователей онлайн

Добавленные фичи
1. graceful выключение сервера с сохранением состояния в файл через /shutdown
2. Загрузка/сохранение истории сообщений и списка пользователей в файлах messages.txt users.txt
3. Очистка файлов истории сообщений и списка пользователей /wipe
3. Авторизация вынесена в отдельный модуль, пароль при вводе не отображается в консоли
4. Авторизация при запуске reciever -> возможность отправлять личные сообщения пользователям через @username
5. Возможность отвечать на сообщения (/reply {msg_number})
