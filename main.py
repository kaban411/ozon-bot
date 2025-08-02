import asyncio, json, os, datetime as dt
from typing import Any

import httpx
import gspread
from google.oauth2.service_account import Credentials
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command

# ─── ENV ───────────────────────────────────────────────────────────────────────
TELEGRAM_BOT_TOKEN      = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID        = int(os.getenv("TELEGRAM_CHAT_ID"))

OZON_CLIENT_ID          = os.getenv("OZON_CLIENT_ID")
OZON_API_KEY            = os.getenv("OZON_API_KEY")

OZON_PERF_CLIENT_ID     = os.getenv("OZON_PERF_CLIENT_ID")
OZON_PERF_CLIENT_SECRET = os.getenv("OZON_PERF_CLIENT_SECRET")

SPREADSHEET_ID          = os.getenv("SPREADSHEET_ID")
GOOGLE_SA_JSON          = json.loads(os.getenv("GOOGLE_SA_JSON"))

# ─── Google Sheets ─────────────────────────────────────────────────────────────
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def get_sheet():
    creds = Credentials.from_service_account_info(GOOGLE_SA_JSON, scopes=SCOPES)
    gc = gspread.authorize(creds)
    return gc.open_by_key(SPREADSHEET_ID)

async def ping_sheet() -> str:
    sh = get_sheet()
    try:
        ws = sh.worksheet("ping")
    except gspread.WorksheetNotFound:
        ws = sh.add_worksheet(title="ping", rows=10, cols=5)
    ts = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ws.update("A1", [["last_ping", ts]])
    return ts

# ─── Ozon Seller API ───────────────────────────────────────────────────────────
SELLER_BASE = "https://api-seller.ozon.ru"

async def ozon_seller_ping() -> Any:
    url = f"{SELLER_BASE}/v1/warehouse/list"
    headers = {
        "Client-Id": OZON_CLIENT_ID,
        "Api-Key"  : OZON_API_KEY,
        "Content-Type": "application/json",
    }
    async with httpx.AsyncClient(timeout=10) as cli:
        r = await cli.post(url, json={}, headers=headers)
        r.raise_for_status()
        return r.json()

# ─── Ozon Performance API ──────────────────────────────────────────────────────
PERF_AUTH = "https://performance.ozon.ru/api/client/token"

async def get_perf_token() -> str:
    payload = {
        "client_id": OZON_PERF_CLIENT_ID,
        "client_secret": OZON_PERF_CLIENT_SECRET,
        "grant_type": "client_credentials",
    }
    async with httpx.AsyncClient(timeout=10) as cli:
        r = await cli.post(PERF_AUTH, data=payload)
        r.raise_for_status()
        return r.json()["access_token"]

# ─── Telegram Bot ──────────────────────────────────────────────────────────────
bot = Bot(token=TELEGRAM_BOT_TOKEN, parse_mode=ParseMode.HTML)   # ← однострочный, «старый» способ
dp  = Dispatcher()

@dp.message(Command("ping"))
async def cmd_ping(m: types.Message):
    ts = await ping_sheet()
    seller = await ozon_seller_ping()
    token  = await get_perf_token()
    await bot.send_message(
        TELEGRAM_CHAT_ID,
        f"✅ <b>pong!</b>\n"
        f"• Sheets OK (время: {ts})\n"
        f"• Seller API ok (warehouses: {len(seller.get('result', []))})\n"
        f"• Perf API token: <code>{token[:12]}…</code>"
    )

# ─── Entrypoint ────────────────────────────────────────────────────────────────
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
