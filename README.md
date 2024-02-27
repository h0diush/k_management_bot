# Телеграм бот на Python с использованием aiogram

Этот бот позволяет создавать, изменять, удалять и изменять статус задачи. Он
использует базу данных PostgreSQL с помощью библиотеки asyncpg для асинхронного
взаимодействия с базой данных. Для работы с базой данных используется
библиотека SQLAlchemy.

## Установка

1. Установите Python 3.8 или выше.
2. Установите [Poetry](https://python-poetry.org/).
3. Клонируйте репозиторий:

```bash
git clone https://github.com/h0diush/task_management_bot.git
```

Перейдите в каталог проекта:

```bash
cd your-repo
```

Установите зависимости:

```bash
poetry install
```

Создайте файл .env в корне проекта и укажите следующие переменные окружения:

```
DB_HOST=your-db-host
DB_PORT=your-db-port
DB_USER=your-db-user
DB_PASS=your-db-password
DB_NAME=your-db-name

BOT_TOKEN=your-bot-token

```
Инициализируйте Alembic в папке с миграциями:
```bash
alembic init -t async database/migrations
```
 Создайте начальную миграцию:
```bash
alembic revision --message="Initial" --autogenerate
```
Примените миграцию к базе данных:
```bash
alembic upgrade head
```
В файле `alembic.ini` добавьте строку с URL-адресом вашей базы данных:
```
sqlalchemy.url = postgresql+asyncpg://user:password@localhost:5432/db-name
```
В файле `database/migrations/env.py` добавьте следующие строки:
```
from models import Base
target_metadata = Base.metadata
```


Запустите бот:

```bash
poetry run python bot.py
```

## Использование:

Меню бота:

```
/tasks - Мои задачи
/help - Информация о боте
/create_task - 'Создать задачу
```

## Структура проекта:

- alembic.ini: Файл конфигурации Alembic для миграций базы данных.
- bot.py: Основной файл бота.
- config_data: Папка с файлами для загрузки конфигурационных данных.
- database: Папка с файлами для работы с базой данных.
- handlers: Папка с файлами для обработки команд бота.
- keyboards: Папка с файлами для создания клавиатур.
- lexicon: Папка с файлами для локализации текста.
- middlewares: Папка с файлами для промежуточных обработчиков.
- models: Папка с файлами для описания моделей базы данных.
- state: Папка с файлами для описания состояний бота.
- utilities: Папка с файлами для вспомогательных функций.
 