from flask import Flask
import requests
import telegram
import time
import threading

app = Flask(__name__)

# توکن بات خود را اینجا وارد کنید
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
CHAT_ID = 'YOUR_CHANNEL_OR_GROUP_CHAT_ID'
CRYPTO_SYMBOL = 'btc'  # نماد ارز دیجیتال مورد نظر (مثلاً بیت‌کوین)

# تنظیمات نوبیتکس
NOBITEX_API_URL = f'https://api.nobitex.ir/v2/orderbook/{CRYPTO_SYMBOL}usdt'

# تابع برای گرفتن قیمت از نوبیتکس
def get_price():
    response = requests.get(NOBITEX_API_URL)
    data = response.json()
    return data['last']

# تابع برای ارسال پیام به تلگرام
def send_message(bot, price):
    bot.send_message(chat_id=CHAT_ID, text=f'The current price of {CRYPTO_SYMBOL} is: ${price}')

# تابع برای به روز رسانی قیمت و ارسال پیام
def update_price():
    bot = telegram.Bot(token=TOKEN)
    while True:
        try:
            price = get_price()
            send_message(bot, price)
            time.sleep(120)  # 2 دقیقه صبر می‌کند
        except Exception as e:
            print(f'Error: {e}')
            time.sleep(120)

# شروع به روز رسانی قیمت در یک ترد جداگانه
threading.Thread(target=update_price).start()

# تنظیمات اصلی فلask
@app.route('/')
def index():
    return "Bot is running!"

if __name__ == '__main__':
    app.run()
