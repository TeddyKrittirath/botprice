import http.server
import socketserver
import threading

# สร้าง Server หลอกๆ เพื่อให้ Render ไม่ปิดบอท
def run_dummy_server():
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", 10000), handler) as httpd:
        httpd.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()

# --- โค้ดเดิมของคุณเริ่มตรงนี้ ---
import requests
import time
...

import requests
import time

# ข้อมูลการเชื่อมต่อ
BOT_TOKEN = "8533277297:AAEioHWirH3siZU0-qx-DmDSCDB3wqqoiRk"
CHAT_ID = "5996259522"
TOKEN_ADDRESS = "EehwFP4EDzfXkz4Sz4wzHd4ydCJ2V7vCMEsh43iopump"

# 🎯 ตั้งค่าราคาและเวลา
TARGET_PRICE_UP = 0.00025
TARGET_PRICE_DOWN = 0.000145
CHECK_INTERVAL = 20  # เช็คทุก 20 วินาที
SUMMARY_INTERVAL = 2 # ทุก 5 นาที (15 รอบ)

count = 0
print("🚀 บอทเริ่มเฝ้าราคาแบบต่อเนื่องแล้ว...")

while True:
    try:
        url = f"https://api.dexscreener.com/latest/dex/tokens/{TOKEN_ADDRESS}"
        response = requests.get(url)
        data = response.json()
        
        if data.get('pairs'):
            current_price = float(data['pairs'][0]['priceUsd'])
            count += 1
            
            # 1. แจ้งเตือนเมื่อราคาถึงเป้า (ส่งเรื่อยๆ ถ้าราคายังอยู่ในเกณฑ์)
            message = ""
            if current_price >= TARGET_PRICE_UP:
                message = f"🚀 ราคาพุ่งถึงเป้า! {current_price} USD"
            elif current_price <= TARGET_PRICE_DOWN:
                message = f"📉 ราคาร่วงถึงจุดซื้อ! {current_price} USD"
            
            if message != "":
                send_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
                requests.get(send_url)
            
            # 2. ส่งสรุปทุก 2 นาที
            if count >= SUMMARY_INTERVAL:
                summary_msg = f"📊 สรุปราคาในรอบ 2 นาที: {current_price} USD"
                send_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={summary_msg}"
                requests.get(send_url)
                count = 0
                print("📢 ส่งรายงานสรุป 2 นาทีเรียบร้อย")

        time.sleep(CHECK_INTERVAL)
        
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")
        time.sleep(CHECK_INTERVAL)
