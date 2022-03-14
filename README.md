# SimbirSoft - сервис для сохранения заметок



Сервис позволяет пользователям добавлять свои заметки с картинками(или без них), удалять их, а также редактировать.
При регистрации пользователь указывает свой email, который будет использоваться при регистрации.

![Без имени](https://user-images.githubusercontent.com/90108557/158039718-8b7e90db-4a9b-4a28-8b8a-5401a78673e2.png)

Зарегистрированные пользователи могут создавать новые заметки.

![Без имени1](https://user-images.githubusercontent.com/90108557/158039757-8f44169b-71fc-4d88-b1d6-239ad19f73ff.png)

![Без имени2png](https://user-images.githubusercontent.com/90108557/158039765-90272093-138e-45be-aca7-5b67ed06b1c5.png)

## Описание архитектуры
- В папке infra лежит docker-compose и nginx
Все ниже указанные папки находятся в директории SimbirSoft
- Приложение about служит для отображения статических страниц "Об авторе" "и Технологии"
- Приложение accounts это кастомная система регистрации
- В приложении core находятся контекстные процессоры: 
1) year-подключается в footer, для отображения текущего года
2) notes_count отображает количество постов пользователя на главной странице
А также view функции для отображения кастомных страниц ошибок и user_filters, которые используются в шаблонах
- Приложение notes работает с заметками
- Папка simbir_note содержит головные urls и настройки проекта
- Папка содержит все шаблоны, используемые в проекте
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
- Изменить настрйки в SimbirSoft/SimbirNote/simbir_note/settings.py
1) Раскомментировать строки 90-95
2) Закомментировать строки 97-106
Выглядеть это должно так:
Было-
![image](https://user-images.githubusercontent.com/90108557/158175851-81ce4734-3910-4367-9e75-ac5cff1a85df.png)

Стало-
![image](https://user-images.githubusercontent.com/90108557/158175915-cc05099c-8c58-441c-a390-d8927c59d594.png)

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

## Инструкция по запуску проекта через докер
+ Открыть Ubuntu и Docker Desktop 
+ В Ubuntu перейти в директорию SimbirNote/infra
+ ``` docker-compose up --build```
+ ``` docker-compose exec web python manage.py makemigrations```
+ ``` docker-compose exec web python manage.py migrate```
+ ``` docker-compose exec web python manage.py runserver```
+ Проект будет открыт локально по адрессу http://127.0.0.1:8000/

## Возможные проблемы:
При запуске с помощью Docker может не загружаться статика(очень много времени пытался понять в чём проблема, так и не разобрался).
Чтобы вы точно смогли взглянуть на проект в его красивой оболочке, запустите проект локально по инструкции описанной выше.

