import os
import asyncio
import logging
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

_bot = None
_app = None
TELEGRAM_AVAILABLE = False
try:
    from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import Application, CallbackQueryHandler
    TELEGRAM_AVAILABLE = True
except ImportError:
    logger.info("python-telegram-bot not installed. Telegram integration disabled.")


def get_bot():
    global _bot, _app
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN.startswith("your_"):
        return None, None
    if _bot is None:
        try:
            from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
            from telegram.ext import Application, CallbackQueryHandler
            _bot = Bot(token=TELEGRAM_BOT_TOKEN)
        except Exception as e:
            logger.warning(f"Telegram init failed: {e}")
            return None, None
    return _bot, _app


def format_order_message(order) -> str:
    # If it's a dict
    if isinstance(order, dict):
        table = order.get("table_number", "?")
        order_id = order.get("id", "?")
        total = order.get("total", 0)
        items = order.get("items", [])
        created_at = order.get("created_at", "")
        status = order.get("status", "pending")
    # If it's an SQLAlchemy object
    else:
        table = order.table.number if order.table else "?"
        order_id = order.id
        total = order.total
        items = []
        for i in order.items:
            mi = i.menu_item
            tps = [{"name_th": oit.topping.name_th, "name_en": oit.topping.name_en} for oit in i.toppings]
            sp_name = ""
            if i.spice_level_id:
                # We can skip looking up spice name just for formatting or fallback to a db query if strictly needed, but dict is better
                pass
            items.append({
                "menu_item_name_th": mi.name_th if mi else "",
                "menu_item_name_en": mi.name_en if mi else "",
                "quantity": i.quantity,
                "unit_price": i.unit_price,
                "notes": i.notes,
                "toppings": tps,
                "spice_level_name_th": sp_name
            })
        created_at = order.created_at.isoformat() if order.created_at else ""
        status = order.status

    try:
        dt = datetime.fromisoformat(created_at).astimezone(timezone.utc)
        time_str = dt.strftime("%H:%M")
    except Exception:
        time_str = "-"

    # Translate status to badge
    badges = {
        "pending": "🆕 รอรับออเดอร์ / Pending",
        "serving": "🔥 กำลังเตรียม / Preparing",
        "done": "✅ เสิร์ฟแล้ว / Served",
        "cancelled": "❌ ยกเลิกแล้ว / Cancelled"
    }
    badge = badges.get(status, status)

    lines = [
        f"🍲 *ออเดอร์ {badge}*",
        f"",
        f"🪑 โต๊ะ / Table: *{table}*",
        f"🔖 หมายเลข / Order ID: `#{order_id}`",
        f"🕐 เวลา / Time: {time_str}",
        f"",
        f"*รายการ / Items:*",
    ]
    for item in items:
        name = item.get("menu_item_name_th", item.get("menu_item_name_en", "Unknown"))
        name_en = item.get("menu_item_name_en", "")
        qty = item.get("quantity", 1)
        price = item.get("unit_price", 0)
        toppings = item.get("toppings", [])
        notes = item.get("notes", "")
        spice_name = item.get("spice_level_name_th", "")

        line = f"• {name}"
        if name_en:
            line += f" / {name_en}"
        line += f" x{qty} — ฿{price * qty:.0f}"
        if spice_name:
            line += f"\n  🌶️ {spice_name}"
        if toppings:
            tp_names = ", ".join(t.get("name_th", t.get("name_en", "")) for t in toppings)
            line += f"\n  🍴 {tp_names}"
        if notes:
            line += f"\n  📝 {notes}"
        lines.append(line)

    lines += [
        f"",
        f"💰 *ยอดรวม / Total: ฿{total:.0f}*",
    ]
    return "\n".join(lines)


def get_keyboard_for_status(order_id: int, status: str):
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    if status == "pending":
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ รับออเดอร์ / Accept", callback_data=f"accept:{order_id}")],
            [InlineKeyboardButton("❌ ยกเลิก / Cancel", callback_data=f"cancel:{order_id}")],
        ])
    elif status == "serving":
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("🍽️ เสิร์ฟแล้ว / Served", callback_data=f"serve:{order_id}")],
            [InlineKeyboardButton("❌ ยกเลิก / Cancel", callback_data=f"cancel:{order_id}")],
        ])
    else:
        # done or cancelled have no buttons
        return None


async def sync_order_message(order_id: int, db):
    bot, _ = get_bot()
    if not bot or not TELEGRAM_CHAT_ID:
        return

    from models import Order
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order or not order.telegram_message_id:
        return

    # To format it properly, we need the dict representation (build_order_out)
    # However we can't import from routers here to avoid circular imports.
    # Therefore, we will format it directly.
    # We will let the route call this function passing the built dict.
    pass

async def sync_telegram_message(order_data: dict, message_id: int):
    """Called from routers to update an existing telegram message."""
    bot, _ = get_bot()
    if not bot or not TELEGRAM_CHAT_ID:
        return

    text = format_order_message(order_data)
    keyboard = get_keyboard_for_status(order_data["id"], order_data["status"])

    try:
        await bot.edit_message_caption(
            chat_id=TELEGRAM_CHAT_ID,
            message_id=message_id,
            caption=text,
            parse_mode="Markdown",
            reply_markup=keyboard
        )
    except Exception as e:
        # Might be a text message without caption
        try:
            await bot.edit_message_text(
                chat_id=TELEGRAM_CHAT_ID,
                message_id=message_id,
                text=text,
                parse_mode="Markdown",
                reply_markup=keyboard
            )
        except Exception as e2:
            logger.warning(f"Telegram sync message update failed: {e2}")


async def notify_new_order(order: dict, db=None):
    bot, _ = get_bot()
    if not bot or not TELEGRAM_CHAT_ID:
        return

    try:
        order_id = order.get("id")
        table = order.get("table_number", "?")
        text = format_order_message(order)
        keyboard = get_keyboard_for_status(order_id, order.get("status", "pending"))

        # ส่งข้อความคั่นออเดอร์ให้เห็นชัดเจน
        separator_text = f"🟩🟩🟩🟩🟩🟩🟩🟩🟩\n🛎️ *ออเดอร์ใหม่ - โต๊ะ {table} 🪑* 🛎️\n🟩🟩🟩🟩🟩🟩🟩🟩🟩"
        try:
            await bot.send_message(
                chat_id=TELEGRAM_CHAT_ID,
                text=separator_text,
                parse_mode="Markdown"
            )
        except Exception as e:
            logger.warning(f"Telegram separator send failed: {e}")

        # ส่งรูปแยกต่างหากทีละรูป เพื่อให้พนักงานที่อ่านไม่ออกดูรูปและจำนวนได้ง่าย
        for item in order.get("items", []):
            url = item.get("menu_item_image_url", "")
            if not url:
                continue
            
            qty = item.get("quantity", 1)
            name = item.get("menu_item_name_th", "Unknown")
            
            # ใช้อีโมจิ 🟢 เพื่อแทนจำนวน เช่น 🟢🟢🟢 สำหรับ 3
            qty_emoji = "🟢" * qty if qty <= 5 else f"🟢 x{qty}"
            
            caption_lines = [
                f"🚨 *จำนวน:* {qty_emoji} ({qty})",
                f"🍲 {name}"
            ]
            if item.get("spice_level_name_th"):
                caption_lines.append(f"🌶️ เผ็ด: {item.get('spice_level_name_th')}")
            if item.get("toppings"):
                t_names = ", ".join(t.get("name_th", "") for t in item.get("toppings"))
                if t_names:
                    caption_lines.append(f"🥢 เพิ่ม: {t_names}")
            if item.get("notes"):
                caption_lines.append(f"📝 หมายเหตุ: {item.get('notes')}")
                
            item_caption = "\n".join(caption_lines)

            photo_data = None
            if url.startswith("http"):
                photo_data = url
            else:
                clean_path = url.lstrip('/')
                if os.path.exists(clean_path):
                    photo_data = open(clean_path, 'rb')
            
            if photo_data:
                try:
                    await bot.send_photo(
                        chat_id=TELEGRAM_CHAT_ID,
                        photo=photo_data,
                        caption=item_caption,
                        parse_mode="Markdown"
                    )
                except Exception as e:
                    logger.warning(f"Telegram photo send failed for {name}: {e}")
                finally:
                    if hasattr(photo_data, 'close'):
                        photo_data.close()

        # หลังจากส่งรูปหมดแล้ว ให้สรุปรายการทั้งหมดพร้อมปุ่มกด
        msg = await bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=text,
            parse_mode="Markdown",
            reply_markup=keyboard,
        )

        # Store message id for future edits
        if msg and db:
            from models import Order
            o = db.query(Order).filter(Order.id == order_id).first()
            if o:
                o.telegram_message_id = msg.message_id
                db.commit()

    except Exception as e:
        logger.warning(f"Telegram notify failed: {e}")


async def handle_callback(update, context):
    query = update.callback_query
    await query.answer()
    data = query.data

    if ":" not in data:
        return

    action, order_id_str = data.split(":", 1)
    order_id = int(order_id_str)

    # Get user who clicked
    user = query.from_user
    fullname = user.first_name
    if user.last_name:
         fullname += f" {user.last_name}"

    import httpx
    base = "http://localhost:8000"

    status_map = {
        "accept": "serving",
        "serve": "done",
        "cancel": "cancelled",
    }
    new_status = status_map.get(action)
    if not new_status:
        return

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.patch(
                f"{base}/api/orders/{order_id}/status",
                json={
                    "status": new_status, 
                    "cancel_reason": f"ยกเลิกโดย {fullname} (Telegram)" if action == "cancel" else ""
                },
            )
        # Note: The PATCH endpoint will call sync_telegram_message which will update the message.
        # We don't need to manually update it here anymore to prevent race conditions.
    except Exception as e:
        logger.warning(f"Telegram callback failed: {e}")


async def start_telegram_bot():
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN.startswith("your_"):
        logger.info("Telegram bot token not configured, skipping bot.")
        return

    try:
        from telegram.ext import Application, CallbackQueryHandler
        global _app
        app_builder = Application.builder().token(TELEGRAM_BOT_TOKEN)
        _app = app_builder.build()
        _app.add_handler(CallbackQueryHandler(handle_callback))
        await _app.initialize()
        await _app.start()
        await _app.updater.start_polling(drop_pending_updates=True)
        logger.info("Telegram bot started.")
    except Exception as e:
        logger.warning(f"Telegram bot failed to start: {e}")


async def stop_telegram_bot():
    global _app
    if _app:
        try:
            await _app.updater.stop()
            await _app.stop()
            await _app.shutdown()
        except Exception:
            pass
