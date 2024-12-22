Запустить проект можно через Docker:

```shell
docker-compose up --build
```

FastAPI: http://localhost:8080/docs

### Проверка работы:
* После запуска проекта, нужно создать админа, используя `scripts/init_admin.py`
* Для корректной проверки нужно **сгенерировать** и **заменить** 3 токена (для админа, для user_1 и для user_2) 
в файле `client.http`. Генерация пользователей и токенов также находится в `client.http`
