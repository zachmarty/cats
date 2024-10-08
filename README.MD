# Проект API для выставки котят

## Описание пректа

Проект представляет собой REST API сервис для сохранения и редактирования записей о котятах, а также для просмотра пород и выставления оценок котятам.

## Подготовка

### Для работы с сервисом необходимо:

- Установить проект
- Установить менеджер зависимостей poetry
- Установить все зависимости командой poetry install
- Активировать виртуальное окружение командой poetry shell
- Создать базу данных в postgresql
- Создать файл переменных окружения .env
- Обозначить там переменные из файла .env.example:
- Применить все миграции командой python manage.py migrate
- Запустить сервер командой python manage.py runserver

## API

Документация по работе с api представлена по урлу /swagger или /redoc. Предварительно для пользования проектом необходимо пройти регистрацию и авторизацию через почту.

## Docker

Для запуска приложения в docker используйте комманды docker-compose build, docker-compose up. После чего к сервису также можно обратиться по адресу http://localhost:8000/

## Тестирование

Тесты описаны в файле cats/tests.py. Для запуска используйте команду python manage.py test.
