# 🍲 หมาล่าหมี POS (MalaMeee POS)

**MalaMeee POS** is a modern Point of Sale (POS) and Customer Self-Ordering system built specifically for Mala / Shabu restaurants. It allows customers to order food directly from their tables using their smartphones, while the kitchen and staff manage orders seamlessly via a real-time Kanban-style dashboard and Telegram bot integration.

*(คลิกที่นี่เพื่ออ่านเอกสารภาษาไทย / Scroll down for Thai version)* 👇

---

## 🚀 Key Features

*   **📱 Customer Self-Ordering:** Mobile-first web interface adapted from popular modern apps. Allows customers to browse menus, select quantities/spice levels, and send orders directly to the kitchen.
*   **🌓 Dark/Light Theme:** Built-in dynamic theme toggling for user comfort.
*   **💻 Real-time POS Dashboard:** A web-based Kanban board for staff to manage orders (`Pending` -> `Serving` -> `Done`) with real-time WebSocket updates.
*   **🤖 Telegram Integration:** Automatically sends new orders to a Telegram group with individual item photos and clear quantity indicators (🟢) tailored for kitchen staff.
*   **🌐 Multi-Language (i18n):** Full support for Thai, English, and Chinese.
*   **🗄️ Easy Menu Management:** Simple menu seeding script to quickly populate and edit the database.
*   **📊 Sales History:** Built-in daily sales summary locked behind a secure PIN gate.
*   **⚡ Zero Setup Execution:** A convenient `run.bat` file automates the installation of dependencies and starts the server instantly.

## 🛠️ Technology Stack

*   **Backend:** Python 3.10+, FastAPI
*   **Database:** SQLite via SQLAlchemy
*   **Real-time:** WebSockets
*   **Frontend:** Vanilla HTML5, CSS3, JavaScript (No heavy frameworks required)
*   **Notifications:** python-telegram-bot

## 📦 How to Run

1.  **Prerequisites:** Ensure you have **Python 3.10 or higher** installed and added to your system PATH.
2.  **Configuration:** 
    *   Rename `.env.example` to `.env`.
    *   Add your Telegram Bot Token and Chat ID to the `.env` file to enable kitchen notifications.
3.  **Start the Application:**
    *   Simply double-click `run.bat` on Windows.
    *   The script will automatically install required libraries, initialize the database (with default seed data), and start the server.
4.  **Access Points:**
    *   Customer Menu: `http://localhost:8000/order`
    *   POS Dashboard: `http://localhost:8000/pos`
    *   Sales History: `http://localhost:8000/history`

## 📝 Customizing the Menu

*   **Adding Items:** Open `seed_data.py` and modify the `menu_items = [...]` list.
*   **Images:** Place your menu images inside the `img/` folder and set the `image_url` property in `seed_data.py` to `/img/filename.extension`.
*   After editing, restart the server or run `python seed_data.py` to reset the database with the new data.

---

<br>

# 🇹🇭 คู่มือการใช้งาน หมาล่าหมี POS (ภาษาไทย)

**หมาล่าหมี POS (MalaMeee POS)** คือระบบจัดการร้านอาหารและระบบสั่งอาหารด้วยตัวเองสำหรับลูกค้าร้านหม่าล่า/ชาบู ระบบถูกออกแบบมาเพื่อให้ลูกค้าสั่งอาหารผ่านมือถือได้ง่ายดาย และให้พนักงานจัดการออเดอร์ในครัวได้อย่างลื่นไหลผ่านแดชบอร์ดแบบเรียลไทม์และการแจ้งเตือนผ่าน Telegram

## 🚀 ฟีเจอร์หลัก

*   **📱 ระบบสั่งอาหารด้วยตัวเอง:** หน้าเว็บสำหรับลูกค้าที่ออกแบบมารองรับหน้าจอมือถือโดยเฉพาะ ลูกค้าสามารถเลือกเมนู ระดับความเผ็ด และท็อปปิ้งได้เอง
*   **🌓 ธีมมืด/สว่าง:** ลูกค้าสามารถกดเปลี่ยนธีม (Theme) หน้าจอได้ตามต้องการ
*   **💻 ระบบจัดการร้าน (POS Dashboard):** แดชบอร์ดแบบคัมบัง (Kanban) สำหรับพนักงาน ในการจัดการออเดอร์ (`รอรับออเดอร์` -> `กำลังเสิร์ฟ` -> `เสร็จสิ้น`) โดยข้อมูลจะอัปเดตเรียลไทม์ ทันทีที่ลูกค้าสั่ง
*   **🤖 เชื่อมต่อ Telegram:** ระบบจะส่งออเดอร์เข้ากลุ่ม Telegram ของพนักงานในครัวอัตโนมัติ โดยแยกส่งรูปภาพทีละรายการ พร้อมสัญลักษณ์ลูกบอล (🟢) บอกจำนวนเพื่อให้พนักงานที่อ่านหนังสือไม่ออกเข้าใจได้ง่าย
*   **🌐 รองรับหลายภาษา:** ระบบรองรับภาษา ไทย, อังกฤษ, และ จีน ในตัว
*   **📊 ประวัติการขาย:** หน้าดูสรุปยอดขายประจำวันและประวัติย้อนหลัง (ป้องกันด้วยรหัส PIN)

## 📦 วิธีการติดตั้งและเปิดใช้งาน

1.  **ความต้องการของระบบ:** ต้องติดตั้ง **Python 3.10 ขึ้นไป** ในเครื่องคอมพิวเตอร์
2.  **การตั้งค่า (Telegram):**
    *   เปลี่ยนชื่อไฟล์ `.env.example` เป็น `.env`
    *   ใส่ `TELEGRAM_BOT_TOKEN` และ `TELEGRAM_CHAT_ID` ลงไปในไฟล์ `.env` ถ้าต้องการให้ระบบส่งออเดอร์เข้าแชท
3.  **เปิดใช้งานระบบ:**
    *   ดับเบิ้ลคลิกเพื่อเปิดไฟล์ `run.bat` (สำหรับ Windows)
    *   ระบบจะทำการติดตั้งไลบรารีที่จำเป็น, สร้างฐานข้อมูลพร้อมเมนูเริ่มต้น, และเปิดรันเซิร์ฟเวอร์ให้อัตโนมัติในคลิกเดียว
4.  **ลิงก์การเข้าใช้งาน:**
    *   หน้าร้านสำหรับลูกค้า: `http://localhost:8000/order`
    *   หน้าจอ POS ของพนักงาน: `http://localhost:8000/pos`
    *   หน้าดูยอดขาย: `http://localhost:8000/history`

## 📝 วิธีการแก้ไขรายชื่อเมนูอาหาร / รูปภาพ

*   **เพิ่มและแก้ไขเมนู:** เปิดไฟล์ `seed_data.py` ขึ้นมา แล้วแก้ไขข้อมูลในบล็อกตัวแปร `menu_items = [...]`
*   **การใส่รูปภาพ:** นำไฟล์รูปภาพที่ต้องการไปวางไว้ในโฟลเดอร์ `img/` แล้วพิมพ์พาธรูปในไฟล์  `seed_data.py` เป็น `/img/ชื่อไฟล์รูป.png`
*   **อัปเดตข้อมูลเข้าระบบ:** หลังจากแก้ไขข้อมูลเสร็จ ให้หยุดการทำงานของเซิร์ฟเวอร์ก่อน แล้วพิมพ์คำสั่ง `python seed_data.py` บนระบบพิมพ์คำสั่ง แล้วจึงรันเซิร์ฟเวอร์ใหม่อีกครั้ง
