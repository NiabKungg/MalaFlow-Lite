/**
 * MalaFlow i18n - Thai / English / Chinese
 */
const TRANSLATIONS = {
  th: {
    // Common
    "brand": "หมาล่าหมี",
    "lang_th": "ไทย",
    "lang_en": "EN",
    "lang_zh": "中文",
    "save": "บันทึก",
    "cancel": "ยกเลิก",
    "confirm": "ยืนยัน",
    "close": "ปิด",
    "loading": "กำลังโหลด...",
    "error": "เกิดข้อผิดพลาด",
    "retry": "ลองใหม่",
    "baht": "฿",
    "table": "โต๊ะ",
    "total": "ยอดรวม",
    "items": "รายการ",
    "notes": "หมายเหตุ",
    "quantity": "จำนวน",
    "price": "ราคา",

    // Order Page
    "select_table": "เลือกโต๊ะ",
    "select_table_desc": "กรุณาเลือกหมายเลขโต๊ะของคุณก่อน",
    "menu": "เมนู",
    "cart": "ตะกร้า",
    "cart_empty": "ยังไม่มีรายการในตะกร้า",
    "add_to_cart": "เพิ่มลงตะกร้า",
    "place_order": "สั่งอาหาร",
    "order_confirm": "ยืนยันการสั่งอาหาร",
    "spice_level": "ระดับความเผ็ด",
    "toppings": "ท็อปปิ้ง",
    "notes_placeholder": "บอกเชฟเพิ่มเติม เช่น ไม่ใส่ผัก",
    "customise": "ปรับแต่ง",
    "extra": "เพิ่ม",
    "order_placed": "สั่งอาหารสำเร็จ! 🎉",
    "order_placed_desc": "ออเดอร์ของคุณถูกส่งไปยังครัวแล้ว",
    "track_order": "ติดตามออเดอร์",
    "change_table": "เปลี่ยนโต๊ะ",

    // Order Status
    "order_status": "สถานะออเดอร์",
    "status_pending": "⏳ รอดำเนินการ",
    "status_serving": "🔥 กำลังเตรียม",
    "status_done": "✅ เสิร์ฟแล้ว",
    "status_cancelled": "❌ ยกเลิก",
    "order_id": "หมายเลขออเดอร์",
    "cancel_reason": "เหตุผลการยกเลิก",
    "back_to_menu": "กลับไปสั่งอาหาร",
    "no_order": "ไม่พบออเดอร์ กรุณาสั่งอาหารใหม่",

    // POS
    "pos_title": "หมาล่าหมี POS",
    "col_pending": "⏳ รอรับออเดอร์",
    "col_serving": "🔥 กำลังเสิร์ฟ",
    "col_done": "✅ เสร็จสิ้น",
    "accept": "รับออเดอร์",
    "serve": "เสิร์ฟแล้ว",
    "cancel_order": "ยกเลิก",
    "cancel_reason_label": "เหตุผลการยกเลิก",
    "cancel_reason_placeholder": "ระบุเหตุผล (ไม่บังคับ)",
    "new_order_toast": "🔔 ออเดอร์ใหม่โต๊ะ",
    "order_updated_toast": "อัพเดทออเดอร์",
    "elapsed": "นานแล้ว",
    "min": "นาที",

    // History
    "history_title": "📊 ประวัติการขาย",
    "enter_pin": "กรอก PIN",
    "pin_label": "รหัส PIN 4 หลัก",
    "pin_wrong": "PIN ไม่ถูกต้อง",
    "date": "วันที่",
    "revenue": "ยอดขาย",
    "orders": "ออเดอร์",
    "cancelled": "ยกเลิก",
    "avg_time": "เวลาเฉลี่ย",
    "history_empty": "ไม่มีประวัติการขาย",
    "expand": "ดูรายการ",
    "daily_summary": "สรุปประจำวัน",
    "filter_date": "กรองตามวันที่",
    "today": "วันนี้",
    "this_week": "สัปดาห์นี้",
  },

  en: {
    "brand": "MalaMeee",
    "lang_th": "ไทย",
    "lang_en": "EN",
    "lang_zh": "中文",
    "save": "Save",
    "cancel": "Cancel",
    "confirm": "Confirm",
    "close": "Close",
    "loading": "Loading...",
    "error": "Error",
    "retry": "Retry",
    "baht": "฿",
    "table": "Table",
    "total": "Total",
    "items": "Items",
    "notes": "Notes",
    "quantity": "Qty",
    "price": "Price",

    "select_table": "Select Table",
    "select_table_desc": "Please select your table number to begin",
    "menu": "Menu",
    "cart": "Cart",
    "cart_empty": "Your cart is empty",
    "add_to_cart": "Add to Cart",
    "place_order": "Place Order",
    "order_confirm": "Confirm Order",
    "spice_level": "Spice Level",
    "toppings": "Toppings",
    "notes_placeholder": "Special instructions for the chef",
    "customise": "Customise",
    "extra": "+",
    "order_placed": "Order Placed! 🎉",
    "order_placed_desc": "Your order has been sent to the kitchen",
    "track_order": "Track Order",
    "change_table": "Change Table",

    "order_status": "Order Status",
    "status_pending": "⏳ Pending",
    "status_serving": "🔥 Preparing",
    "status_done": "✅ Served",
    "status_cancelled": "❌ Cancelled",
    "order_id": "Order ID",
    "cancel_reason": "Cancellation Reason",
    "back_to_menu": "Back to Menu",
    "no_order": "No order found. Please place an order.",

    "pos_title": "MalaMeee POS",
    "col_pending": "⏳ Pending",
    "col_serving": "🔥 Serving",
    "col_done": "✅ Done",
    "accept": "Accept",
    "serve": "Served",
    "cancel_order": "Cancel",
    "cancel_reason_label": "Cancellation Reason",
    "cancel_reason_placeholder": "Reason (optional)",
    "new_order_toast": "🔔 New order Table",
    "order_updated_toast": "Order updated",
    "elapsed": "Elapsed",
    "min": "min",

    "history_title": "📊 Sales History",
    "enter_pin": "Enter PIN",
    "pin_label": "4-digit PIN",
    "pin_wrong": "Incorrect PIN",
    "date": "Date",
    "revenue": "Revenue",
    "orders": "Orders",
    "cancelled": "Cancelled",
    "avg_time": "Avg Time",
    "history_empty": "No sales history",
    "expand": "View Items",
    "daily_summary": "Daily Summary",
    "filter_date": "Filter by Date",
    "today": "Today",
    "this_week": "This Week",
  },

  zh: {
    "brand": "MalaMeee",
    "lang_th": "ไทย",
    "lang_en": "EN",
    "lang_zh": "中文",
    "save": "保存",
    "cancel": "取消",
    "confirm": "确认",
    "close": "关闭",
    "loading": "加载中...",
    "error": "错误",
    "retry": "重试",
    "baht": "฿",
    "table": "桌号",
    "total": "总计",
    "items": "菜品",
    "notes": "备注",
    "quantity": "数量",
    "price": "价格",

    "select_table": "选择桌号",
    "select_table_desc": "请先选择您的桌号",
    "menu": "菜单",
    "cart": "购物车",
    "cart_empty": "购物车为空",
    "add_to_cart": "加入购物车",
    "place_order": "下单",
    "order_confirm": "确认订单",
    "spice_level": "辣度",
    "toppings": "加料",
    "notes_placeholder": "给厨师的特别要求",
    "customise": "定制",
    "extra": "+",
    "order_placed": "下单成功！🎉",
    "order_placed_desc": "您的订单已发送至厨房",
    "track_order": "跟踪订单",
    "change_table": "更换桌号",

    "order_status": "订单状态",
    "status_pending": "⏳ 等待处理",
    "status_serving": "🔥 准备中",
    "status_done": "✅ 已上菜",
    "status_cancelled": "❌ 已取消",
    "order_id": "订单号",
    "cancel_reason": "取消原因",
    "back_to_menu": "返回菜单",
    "no_order": "未找到订单，请重新下单",

    "pos_title": "MalaMeee POS",
    "col_pending": "⏳ 待处理",
    "col_serving": "🔥 制作中",
    "col_done": "✅ 已完成",
    "accept": "接受订单",
    "serve": "已上菜",
    "cancel_order": "取消",
    "cancel_reason_label": "取消原因",
    "cancel_reason_placeholder": "原因（可选）",
    "new_order_toast": "🔔 新订单 桌",
    "order_updated_toast": "订单已更新",
    "elapsed": "已过",
    "min": "分钟",

    "history_title": "📊 销售记录",
    "enter_pin": "输入PIN码",
    "pin_label": "4位PIN码",
    "pin_wrong": "PIN码不正确",
    "date": "日期",
    "revenue": "营业额",
    "orders": "订单数",
    "cancelled": "取消",
    "avg_time": "平均时间",
    "history_empty": "暂无销售记录",
    "expand": "查看菜品",
    "daily_summary": "每日汇总",
    "filter_date": "按日期筛选",
    "today": "今天",
    "this_week": "本周",
  }
};

const I18N = {
  currentLang: localStorage.getItem('malaflow_lang') || 'th',

  t(key) {
    return TRANSLATIONS[this.currentLang]?.[key] || TRANSLATIONS['en']?.[key] || key;
  },

  setLang(lang) {
    if (!TRANSLATIONS[lang]) return;
    this.currentLang = lang;
    localStorage.setItem('malaflow_lang', lang);
    this.applyAll();
    document.dispatchEvent(new CustomEvent('langChange', { detail: { lang } }));
  },

  applyAll() {
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      el.textContent = this.t(key);
    });
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
      el.placeholder = this.t(el.getAttribute('data-i18n-placeholder'));
    });
    document.querySelectorAll('[data-i18n-title]').forEach(el => {
      el.title = this.t(el.getAttribute('data-i18n-title'));
    });
    // Update lang buttons
    document.querySelectorAll('.lang-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.lang === this.currentLang);
    });
  },

  itemName(item) {
    const k = `name_${this.currentLang}`;
    return item[k] || item.name_th || item.name_en || '';
  },

  itemDesc(item) {
    const k = `description_${this.currentLang}`;
    return item[k] || item.description_th || item.description_en || '';
  }
};

// Auto-init on DOM ready
document.addEventListener('DOMContentLoaded', () => {
  I18N.applyAll();

  // Wire language buttons
  document.querySelectorAll('.lang-btn').forEach(btn => {
    btn.addEventListener('click', () => I18N.setLang(btn.dataset.lang));
  });
});

// Toast helper
function showToast(message, type = 'info', duration = 3500) {
  let container = document.querySelector('.toast-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
  }
  const icons = { success: '✅', error: '❌', warning: '⚠️', info: 'ℹ️' };
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `<span>${icons[type] || 'ℹ️'}</span><span>${message}</span>`;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.animation = 'slideInRight 0.3s ease-out reverse';
    setTimeout(() => toast.remove(), 280);
  }, duration);
}

// WebSocket helper
function createWS(onMessage) {
  const proto = location.protocol === 'https:' ? 'wss' : 'ws';
  const ws = new WebSocket(`${proto}://${location.host}/ws`);
  ws.onmessage = e => {
    try { onMessage(JSON.parse(e.data)); } catch {}
  };
  ws.onclose = () => setTimeout(() => createWS(onMessage), 3000);
  return ws;
}
