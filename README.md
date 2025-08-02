# Ozon ↔ Telegram ↔ Google Sheets бот

**Что делает**  
После запуска бот принимает команду `/ping` в Telegram, записывает текущую дату/время в лист `ping` вашей Google‑таблицы и отвечает сообщением «pong!», подтверждая, что все соединения (Sheets, Ozon Seller API, Ozon Performance API) работают.

## Быстрый старт

1. Создайте Google‑таблицу и дайте доступ сервис‑аккаунту (email в JSON‑файле).  
2. Создайте Telegram‑бота через @BotFather.  
3. Получите ключи Seller API и Performance API Ozon.  
4. Заведите аккаунт на **Render.com**.

### Шаг 1: залить код на GitHub  
* Распакуйте архив, создайте новый репозиторий на GitHub, перетащите файлы (или используйте «Upload files»).

### Шаг 2: развернуть на Render  
1. На Render нажмите **New → Blueprint** и вставьте содержимое `render.yaml` (или загрузите файл).  
2. Замените `repo:` на URL вашего GitHub‐репозитория.  
3. Нажмите **Apply**. Render попросит ввести переменные окружения — скопируйте их из таблицы ниже.  
4. После деплоя напишите боту `/ping`.

| Переменная | Что вставить |
|------------|-------------|
| TELEGRAM_BOT_TOKEN | токен из BotFather |
| TELEGRAM_CHAT_ID   | числовой ID вашего чата |
| OZON_CLIENT_ID     | ID продавца |
| OZON_API_KEY       | API‑ключ |
| OZON_PERF_CLIENT_ID | client_id рекламы |
| OZON_PERF_CLIENT_SECRET | client_secret рекламы |
| SPREADSHEET_ID     | часть URL таблицы между `/d/` и `/edit` |
| GOOGLE_SA_JSON     | ВЕСЬ текст JSON сервис‑аккаунта в одну строку |

Готово! Бот онлайн 24 × 7 на бесплатном плане Render.
