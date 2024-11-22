Управление Библиотекой с использованием FastAPI и PostgreSQL
Этот проект представляет собой RESTful API и позволяет выполнять операции CRUD над книгами, а также управлять их статусами.

Структура проекта
Проект организован следующим образом:

src/api/v1/endpoints.py: Содержит маршруты API.

src/schemas/book.py: Определяет схемы данных для книг.

src/schemas/response.py: Определяет схемы ответов API.

src/service/service.py: Содержит бизнес-логику для управления книгами.

src/models/books.py: Определяет модели SQLAlchemy для книг.

tests/: Содержит тесты для API.

Запуск проекта
Проект можно запустить с использованием Docker Compose. Убедитесь, что у вас установлены Docker и Docker Compose.

Шаги для запуска:
Склонируйте репозиторий:

bash
Copy
git clone https://github.com/alkibin/library_api.git
cd library-management
Создайте файл .env:
Создайте файл .env в корне проекта и добавьте следующие переменные окружения:

env
Copy
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_DB=library_db
POSTGRES_HOST=db
POSTGRES_PORT=5432
Запустите Docker Compose:

docker-compose up -d --build
Это создаст и запустит контейнеры для приложения и базы данных.


С приложением можно повзаимодействовать через сваггер на localhost:81/api/openapi