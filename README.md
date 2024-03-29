![Image alt](https://github.com/blakkheart/api_yamdb/raw/master/api_yamdb/static/logo1.png)
## <p align="center"> :trophy:  Совместный проект 'API_Yamdb' :trophy: </p>

### В разработке проекта участвовали: <br>

#### :sunglasses: *Тимлид - Первый разработчик: [Влад](https://github.com/blakkheart)* <br>
#### :sunglasses: *Второй разработчик: [Ринат](https://github.com/Rinat-Khusainov)*  <br>
#### :sunglasses: *Третий разработчик: [Ден](https://github.com/Den4u)*  <br>


### Выполненные задачи: 
 - Бэкенд проекта и API для него.
---
### *Оглавление:* 
1. [Описание проекта.](#title1)
2. [Как запустить проект.](#title2)
3. [Документация к проекту.](#title3)
4.  - [Пример регистрация новых пользователей.](#title4) 
    - [Пример cоздания пользователя администратором.](#title5)
---


### 1. <a id="title1">Описание проекта:</a>
- Проект **YaMDb** собирает отзывы пользователей на различные произведения.

- Произведения делятся на категории, им может быть присвоен жанр из списка предустановленных.

- Пользователи могут оставлять к произведениям текстовые отзывы и комментарии к ним, ставить оценку.

- Из пользовательских оценок формируется рейтинг (на одно произведение пользователь может оставить только один отзыв).

- Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

---
### 2. <a id="title2">Как запустить проект</a>

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Den4u/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

---
### 3. <a id="title3">Документация к проекту. </a>
###  <p align="center"> [---> Доступна после запуска проекта <---](http://127.0.0.1:8000/redoc/) </p>
---

### 4.1  <a id="title4">Пример регистрация новых пользователей.</a>

1. Пользователь отправляет POST-запрос с параметрами email и username на эндпоинт /api/v1/auth/signup/.

2. Сервис YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на указанный адрес email.

3. Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт /api/v1/auth/token/, в ответе на запрос ему приходит token (JWT-токен).


В результате пользователь получает токен и может работать с API проекта, отправляя этот токен с каждым запросом. 
После регистрации и получения токена пользователь может отправить PATCH-запрос на эндпоинт /api/v1/users/me/ и заполнить поля в своём профайле (описание полей — в документации).

---
### 4.2 <a id="title5">Пример cоздания пользователя администратором.</a>

1. Пользователей создаёт администратор — через админ-зону сайта или через POST-запрос на специальный эндпоинт api/v1/users/ (описание полей запроса для этого случая есть в документации). При создании пользователя не предполагается автоматическая отправка письма пользователю с кодом подтверждения. 


2. После этого пользователь должен самостоятельно отправить свой email и username на эндпоинт /api/v1/auth/signup/ , в ответ ему должно прийти письмо с кодом подтверждения.


3. Далее пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт /api/v1/auth/token/, в ответе на запрос ему приходит token (JWT-токен), как и при самостоятельной регистрации.
