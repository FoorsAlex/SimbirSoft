# SimbirSoft - сервис для сохранения заметок



Сервис позволяет пользователям добавлять свои заметки с картинками(или без них), удалять их, а также редактировать.
При регистрации пользователь указывает свой email, который будет использоваться при регистрации.

![Без имени](https://user-images.githubusercontent.com/90108557/158039718-8b7e90db-4a9b-4a28-8b8a-5401a78673e2.png)

Зарегистрированные пользователи могут создавать новые заметки.

![Без имени1](https://user-images.githubusercontent.com/90108557/158039757-8f44169b-71fc-4d88-b1d6-239ad19f73ff.png)

![Без имени2png](https://user-images.githubusercontent.com/90108557/158039765-90272093-138e-45be-aca7-5b67ed06b1c5.png)



## Запуск проекта локально
- Склонировать проект и перейти в папку проекта

```bash
https://github.com/FoorsAlex/SimbirSoft.git
cd SimbirNote/
```
- Установить и активировать виртуальное окружение, или создать новый проект в PyCharm

```bash
python -m venv venv
source venv\bin\activate
```

- Установить зависимости из файла **requirements.txt**
 
```bash
pip install -r requirements.txt
``` 
- В папке с файлом manage.py выполнить команды:

```bash
python manage.py makemigrations
python manage.py migrate
```
- Создать пользователя с неограниченными правами:

```bash
python manage.py createsuperuser
```
- Запустить web-сервер на локальной машине:

```bash
python manage.py runserver
```



## Docker инструкции
- Установить Docker и получить образ

```
docker pull dangerousmonk/SimbirSoft:latest
```

Проект можно развернуть используя контейнеризацию с помощью Docker  
Параметры запуска описаны в `infra/docker-compose.yml`.

При запуске создаются три контейнера:

 - контейнер базы данных **db**
 - контейнер приложения **backend**
 - контейнер web-сервера **nginx**

Для развертывания контейнеров необходимо:


- Создать и сохранить переменные окружения в **.env** файл, образец ниже
```bash
DB_ENGINE=django.db.backends.postgresql
DB_NAME=foodgram_exmpl
POSTGRES_USER=user
POSTGRES_PASSWORD=12345
POSTGRES_DB=yamdb #имя БД которое возьмет образ postgres
DB_HOST=db
DB_PORT=5432
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=someuser@gmail.com
EMAIL_HOST_PASSWORD=secretpassword
```

- Запустить docker-compose

```bash
docker-compose up
```
- Выполнить миграции и подключить статику

```bash
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py collectstatic --noinput
```
- Создать superuser

```bash
docker-compose exec backend python manage.py createsuperuser
```
## Возможные проблемы:
При запуске с помощью Docker может не загружаться статика(очень много времени пытался понять в чём проблема, так и не разобрался).
Чтобы вы точно смогли взглянуть на проект в его красивой оболочке, я добавил в SimbirSoft/SimbirNote/simbir_note/settings вот эти закомментированные строки:

![image](https://user-images.githubusercontent.com/90108557/158039983-bec60c94-c869-469b-a656-e0f9d782a18d.png)

Вам нужно их раскомментировать и закоментировать строки ниже, должно получиться вот так:

![image](https://user-images.githubusercontent.com/90108557/158040024-1076329a-f06b-4982-96ee-6a4ad3bf4fbe.png)

- После выполнить команды:
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
