# Blogicum

## Описание:

Социальная сеть для публикации дневников. Сайт, на котором пользователь может создать свою страницу и публиковать на ней сообщения в определенной категории.
Также реализована возможность добавления комментариев, регистрация и авторизация пользователей.

### Использованные технологии:

Python 3.9.10
Django 3.2


### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Emphori-a/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

