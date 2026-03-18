# lyceum-attendance

Телеграм-бот для запису відвідування учнями Березанського ліцею №3.

## Функції

- Надсилання щоденного звіту про відвідування
- Панель адміністратора для перегляду звітів
- Автоматичне ранкове нагадування
- Налаштування профілю користувача

## Технологічний стек

- python - основна мова розробки
- aiogram - фрейморк для Telegram-ботів
- sqlalchemy - ORM для БД
- postgresql - база даних

## Змінні середовища

```
TOKEN=токен_телеграм_бота

POSTGRESQL_URL="postgresql+asyncpg://secret:secret@secret:secret/secret"

POSTGRES_USER="юзернейм_бд"
POSTGRES_PASSWORD="пароль_бд"
POSTGRES_DB="назва_бд"
```

## Запуск

Передумови:

- docker
- docker-compose

Запуск:

```bash
sudo docker-compose up --build
```

Зупинка:

```
sudo docker-compose down
```

## Docker

Докер містить два сервіси:

- **bot**: телеграм бот на Python
- **db**: база даних PostgreSQL

## База даних

БД містить декілька таблиць:

- **admins** - список адміністраторів
- **forms** - список навчальних класів
- **reports** - список звітів
- **users** - список користувачів

## Ліцензія

Проєкт розповсюджується під [MIT License](./LICENSE).
