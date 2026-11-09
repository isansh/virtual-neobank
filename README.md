# virtual-neobank
Модель User
- `id` (INTEGER / UUID) — унікальний ідентифікатор
    
- `email` (STRING, unique)
    
- `password_hash` (STRING) — хешований пароль (не відкритий текст!)
    
- `full_name` (STRING) — ПІБ користувача
    
- `phone_number` (STRING) — номер телефону
    
- `kyc_status` (STRING) — `pending`, `verified`, `rejected` (для KYC)
    
- `created_at` (TIMESTAMP)
  
  Ендпоінти
- `POST /api/auth/register` — реєстрація нового акаунту
    
- `POST /api/auth/login` — вхід і отримання `JWT-токена`
    
- `GET /api/users/me` — отримання профілю поточного авторизованого користувача (потребує JWT в заголовку `Authorization: Bearer <token>`)
    
- `PUT /api/users/me` — оновлення даних профілю / проходження KYC

### Структура та призначення файлів (`backend/`)

- **`app/main.py`** — Головна точка входу в додаток. Ініціалізує FastAPI, створює таблиці в базі даних при запуску та підключає всі роутери (`auth` і `users`).
    
- **`app/core/database.py`** — Налаштування підключення до бази даних (SQLite). Створює engine, сесії БД та функцію-залежність `get_db()` для отримання доступу до БД у запитах.
    
- **`app/core/security.py`** — Модуль безпеки. Відповідає за хешування паролів (`bcrypt`), їх перевірку при вході, а також генерацію та декодування JWT-токенів.
    
- **`app/models/user.py`** — SQLAlchemy-модель `User`. Визначає структуру таблиці `users` у базі даних (поля `id`, `email`, `hashed_password`, `full_name`, `phone_number`, `kyc_status`, `created_at`).
    
- **`app/schemas/user.py`** — Pydantic-схеми (DTO). Валідують вхідні дані від клієнта (реєстрація, вхід, оновлення) та формують безпечну структуру відповіді (повертають дані користувача без хешу пароля).
    
- **`app/routers/deps.py`** — Залежності авторизації (Middleware/Dependency). Витягує JWT-токен із заголовка `Authorization: Bearer <token>`, перевіряє його та повертає об'єкт поточного залогіненого користувача (`get_current_user`).
    
- **`app/routers/auth.py`** — Роутер автентифікації. Містить ендпоінти реєстрації (`POST /api/auth/register`) та входу (`POST /api/auth/login`).
    
- **`app/routers/users.py`** — Роутер управління профілем. Містить ендпоінти отримання профілю поточного користувача (`GET /api/users/me`) та оновлення даних/KYC-статусу (`PUT /api/users/me`).
    
- **`requirements.txt`** — Список усіх необхідних Python-бібліотек (FastAPI, Uvicorn, SQLAlchemy, Passlib тощо) для швидкого розгортання проєкту.

Як я почала з цим роботу
клонуємо репозиторій, створюємо собі гілочку
git clone https://github.com/isansh/virtual-neobank.git
git checkout -b feature/auth-and-user-profile

далі пайтон в бекенді
cd backend
 python -m venv venv
 venv\Scripts\activate
 pip install -r requirements.txt
 
запуск свагера
uvicorn app.main:app --reload