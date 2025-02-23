import requests
from flask import Flask, request
from atproto import Client

# تنظیمات بات
BLUESKY_HANDLE = "corocodil.bsky.social"  # نام کاربری بلواسکای
BLUESKY_APP_PASSWORD = "hprd-bw6c-wklq-tysk"  # رمز عبور مخصوص اپ (از تنظیمات بلواسکای بگیر)
API_URL = "https://brsapi.ir/FreeTsetmcBourseApi/Api_Free_Gold_Currency_v2.json"  # API قیمت‌ها از brsapi.ir

# راه‌اندازی کلاینت بلواسکای
client = Client()
client.login(BLUESKY_HANDLE, BLUESKY_APP_PASSWORD)

# ایجاد اپلیکیشن Flask
app = Flask(__name__)

def get_prices():
    """دریافت قیمت دلار و طلا از brsapi.ir"""
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        try:
            dollar_price = data["Currency"][0]["Price"]  # قیمت دلار
            gold_price = data["Gold"][0]["Price"]  # قیمت طلا
            return f"💰 قیمت دلار: {dollar_price} تومان\n🔶 قیمت طلای ۱۸ عیار: {gold_price} تومان"
        except (KeyError, IndexError):
            return "❌ خطا در پردازش اطلاعات دریافتی!"
    return "❌ نتوانستم قیمت را دریافت کنم."

@app.route("/webhook", methods=["POST"])
def webhook():
    """دریافت پیام‌های بلواسکای و ارسال پاسخ"""
    data = request.json
    text = data.get("text", "").lower()
    author = data.get("author", "")

    if "دلار" in text or "طلا" in text:
        price_info = get_prices()
        response_text = f"👋 سلام @{author}\n{price_info}"
        client.post(text=response_text)
    
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
