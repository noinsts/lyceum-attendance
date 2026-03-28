<div align="center">

# 📊 lyceum-attendance

[![Python](https://img.shields.io/badge/Python-3.12+-blue)](https://python.org/)
[![aiogram](https://img.shields.io/badge/aiogram-3.x-green)](https://aiogram.dev/)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

Telegram-бот для автоматизації обліку щоденного відвідування учнями Березанського ліцею №3.

</div>

## ✨ Ключові функції

- ✍️ **Швидка подача звітів**: Вчителі вводять лише цифри відсутніх та хворих.
- 🔔 **Розумні нагадування**: Автоматичний пінг о **08:55** для тих, хто забув подати звіт.
- 👑 **Адмін-панель**: Перегляд зведеної статистики для адміністрації закладу.
- 🐳 **Docker-ready**: Запуск всього середовища однією командою де завгодно.

## 📱 Інтерфейс бота

<div align="center">
<table>
  <tr>
    <td width="50%" align="center">
      <img src="assets/hub.jpg" alt="Подача звіту" width="100%"/>
      <p><i>Головне меню та реєстрація</i></p>
    </td>
    <td width="50%" align="center">
      <img src="assets/report.jpg" alt="Адмінка" width="100%"/>
      <p><i>Подача звіту вчителем</i></p>
    </td>
  </tr>
</table>
</div>

## 🚀 Quickstart

### 1. Налаштування змінних оточення

Створіть файл `.env` у корені проєкту (використайте `.env.example` як зразок)

### 2. Запуск

```bash
# Запуск
sudo docker-compose up --build

# Зупинка
sudo docker-compose down
```

## 📝 Документація

Розширена документація доступна в папці [`docs/`](/docs/).

<p align="center">
  MIT License © 2026 <a href="https://github.com/noints">noinsts</a>
</p>
