import threading
import time
import re
import json
import cloudscraper
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ KKTIX 監控中（使用 cloudscraper 模擬瀏覽器，解決 403）"

def ticket_checker():
    print("🧵 背景執行緒已啟動！準備開始抓票...")
    event_url = "https://kktix.com/events/16db8dfa/registrations/new"
    scraper = cloudscraper.create_scraper()  # 模擬真實瀏覽器，繞過 Cloudflare

    while True:
        print(f"🔍 正在檢查票務狀態：{event_url}")
        try:
            response = scraper.get(event_url)
            if response.status_code != 200:
                print(f"⚠️ 無法取得頁面，狀態碼：{response.status_code}")
            else:
                html = response.text
                match = re.search(r'window\.__INITIAL_STATE__ = ({.*?});', html)
                if match:
                    data = json.loads(match.group(1))
                    tickets = data.get("registration", {}).get("ticket_types", [])
                    print("🎟️ 票種資訊：")
                    for ticket in tickets:
                        name = ticket.get("name", "未知票種")
                        remaining = ticket.get("remaining_quantity", 0)
                        total = ticket.get("quantity", 0)
                        print(f"👉 {name}: 剩餘 {remaining}/{total} 張")
                else:
                    print("❌ 找不到票務資料 (__INITIAL_STATE__)")
        except Exception as e:
            print("⚠️ 發生錯誤：", e)
        print("⏳ 等待 5 秒後再次檢查...\n")
        time.sleep(5)

if __name__ == '__main__':
    print("🚀 啟動 Flask 與背景票務任務...")
    threading.Thread(target=ticket_checker, daemon=True).start()
    app.run(host='0.0.0.0', port=10000)
