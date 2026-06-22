# API управления пользователями и правами доступа
## Описание проекта

Проект представляет собой REST API, разработанное на FastAPI, 
для управления пользователями и системой разграничения доступа.

## Используемые технологии

- Python 3.11
- FastAPI
- SQLAlchemy (Async)
- PostgreSQL
- Alembic
- Pydantic
- JWT

## Структура управления доступом

Доступ реализован с помощью трех сущностей:

- roles - роли пользователей;
- business_elements - бизнес-элементы системы;
- access_rules - правила доступа роли к бизнес-элементу.

Для каждого элемента доступны следующие разрешения:

- create_permission - создание;
- read_permission - просмотр своих данных;
- read_all_permission - просмотр всех данных;
- update_permission - изменение своих данных;
- update_all_permission - изменение любых данных;
- delete_permission - удаление своих данных;
- delete_all_permission - удаление любых данных.

Перед выполнением запроса PermissionChecker определяет необходимое 
разрешение по HTTP-методу и проверяет его наличие у текущего пользователя.

## Запуск проекта
### 1. Клонировать репозиторий

```bash
git clone git@github.com:REBIZ1/Auth.git
```

### 2. Создать виртуальное окружение

```bash
python -m venv .venv
```

Linux / macOS

```bash
source .venv/bin/activate
```

Windows

```bash
.venv\Scripts\activate
```

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

### 4. Создать файл .env

Заполнить необходимые параметры подключения к базе данных и настройки JWT.

### 5. Выполнить миграции

```bash
alembic upgrade head
```

### 6. Запустить приложение

```bash
python -m src.main
```
