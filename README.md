# Описание проета продуктового помощника Foodgram
На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд. Для удобного поиска рецептов предусмотрена фильтрация по тегам.

## Использованные технологии
### Основные:
- Django 3.2.15
- Docker 20.10.17
- Docker-compose 2.10.2
- Gunicorn
- Nginx 1.19.3
- PostgreSQL 13.0

### Дополнительные:
- django-colorfield 0.7.2
- django-filter 22.1
- Django REST framework 3.14.0
- Simple JWT 4.8.0
- djoser 2.1.0

## Запуск проекта локально
1. В директории backend/foodgram/foodgram создайте .env и заполните переменными окружения.
```
DEBUG=''
ALLOWED_HOSTS='localhost 127.0.0.1 http://localhost:3000 backend'
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=Admin
POSTGRES_PASSWORD=qweqwe
DB_HOST=db
DB_PORT=5432
SECRET_KEY='django-insecure-0q@sllks6!(0@04u-yl8b1i2qn^ktd+txn8ec43+-4t(^paw9b'
```

2. Перед началом запуска проекта, убедитесь, что у вас установлен [Docker](https://docs.docker.com/engine/install/).

3. Клонируйте [репозитарий foodgram-project-react с GitHub](https://hub.docker.com/).
```
git clone git@github.com:Inozem/foodgram-project-react.git
```

4. Для развертывания проекта войдите в папку infra/ и выполните следующую команду:
```
docker-compose up -d --build
```

5. После того как все контейнеры будут развернуты, необходимо выполнить миграции.
```
docker-compose exec backend python manage.py migrate
```

6. Создайте суперпользователя.
```
docker-compose exec backend python manage.py createsuperuser
```

7. Соберите статику.
```
docker-compose exec backend python manage.py collectstatic --no-input
```

8. Загрузите список ингредиентов в базу данных.
```
docker-compose exec backend python manage.py add_ingredients
```

9. Перед тем как приступить к тестированию непосредственно функционала сайта, войдите в [панель администратора](http://localhost/admin/), используя логин и пароль суперпользователя, и создайте несколько тегов и рецептов. Теперь все готово, зарегистрируйтесь новым пользователем на [сайте](http://localhost/) и приступайте к тестированию.

10. Для того, чтобы остановить работу контейноров - воспользуйтесь следующей командой:
```
docker-compose down -v 
```
