import requests
import re
import json
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def check_kktix_ticket(event_url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    print(f"🔍 正在檢查票務狀態：{event_url}")
    response = requests.get(event_url, headers=headers, verify=False)

    if response.status_code != 200:
        print(f"⚠️ 無法取得頁面，狀態碼：{response.status_code}")
        return

    html = response.text

    match = re.search(r'window\.__INITIAL_STATE__ = ({.*?});', html)
    if not match:
        print("❌ 找不到票務資料 (__INITIAL_STATE__)")
        return

    try:
        data = json.loads(match.group(1))
        tickets = data.get("registration", {}).get("ticket_types", [])
        
        if not tickets:
            print("❌ 沒有找到票種資料")
            return

        print("🎟️ 票種資訊：")
        for ticket in tickets:
            name = ticket.get("name", "未知票種")
            remaining = ticket.get("remaining_quantity", 0)
            total = ticket.get("quantity", 0)
            print(f"👉 {name}: 剩餘 {remaining}/{total} 張")

    except Exception as e:
        print("⚠️ 解析票務資料時發生錯誤：", e)

if __name__ == "__main__":
    event_url = "https://kktix.com/events/16db8dfa/registrations/new"
    
    while True:
        check_kktix_ticket(event_url)
        print("⏳ 等待 10 秒後再次檢查...\n")
        time.sleep(5)
