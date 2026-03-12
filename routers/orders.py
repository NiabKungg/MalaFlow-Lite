import asyncio
import json
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from database import get_db
from models import Order, OrderItem, OrderItemTopping, MenuItem, SpiceLevel, Topping, TableInfo
from schemas import OrderCreate, OrderOut, OrderItemOut, OrderStatusUpdate, ToppingSnap
from websocket_manager import manager

router = APIRouter(prefix="/api", tags=["orders"])


def build_order_out(order: Order) -> dict:
    items_out = []
    for oi in order.items:
        mi = oi.menu_item
        sl = None
        if oi.spice_level_id:
            # fetch spice level name from id stored on item
            pass
        toppings_out = []
        for oit in oi.toppings:
            t = oit.topping
            toppings_out.append({
                "id": t.id,
                "name_th": t.name_th,
                "name_en": t.name_en,
                "name_zh": t.name_zh,
                "price": t.price,
            })
        items_out.append({
            "id": oi.id,
            "menu_item_id": oi.menu_item_id,
            "menu_item_name_th": mi.name_th if mi else "",
            "menu_item_name_en": mi.name_en if mi else "",
            "menu_item_name_zh": mi.name_zh if mi else "",
            "menu_item_image_url": mi.image_url if mi else "",
            "spice_level_id": oi.spice_level_id,
            "spice_level_name_th": "",
            "spice_level_name_en": "",
            "quantity": oi.quantity,
            "unit_price": oi.unit_price,
            "notes": oi.notes,
            "toppings": toppings_out,
        })
    table = order.table
    return {
        "id": order.id,
        "table_id": order.table_id,
        "table_number": table.number if table else 0,
        "status": order.status,
        "total": order.total,
        "cancel_reason": order.cancel_reason or "",
        "created_at": order.created_at.isoformat() if order.created_at else "",
        "updated_at": order.updated_at.isoformat() if order.updated_at else "",
        "items": items_out,
    }


@router.post("/orders")
async def create_order(payload: OrderCreate, db: Session = Depends(get_db)):
    table = db.query(TableInfo).filter(TableInfo.id == payload.table_id).first()
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")

    total = 0.0
    order = Order(table_id=payload.table_id, status="pending", total=0.0)
    db.add(order)
    db.flush()

    for item_data in payload.items:
        mi = db.query(MenuItem).filter(MenuItem.id == item_data.menu_item_id).first()
        if not mi:
            raise HTTPException(status_code=404, detail=f"Menu item {item_data.menu_item_id} not found")
        
        spice_extra = 0.0
        if item_data.spice_level_id:
            sl = db.query(SpiceLevel).filter(SpiceLevel.id == item_data.spice_level_id).first()
            if sl:
                spice_extra = sl.extra_price

        topping_total = 0.0
        for tp_data in item_data.toppings:
            tp = db.query(Topping).filter(Topping.id == tp_data.topping_id).first()
            if tp:
                topping_total += tp.price

        unit_price = mi.price + spice_extra + topping_total
        total += unit_price * item_data.quantity

        oi = OrderItem(
            order_id=order.id,
            menu_item_id=mi.id,
            spice_level_id=item_data.spice_level_id,
            quantity=item_data.quantity,
            unit_price=unit_price,
            notes=item_data.notes,
        )
        db.add(oi)
        db.flush()

        for tp_data in item_data.toppings:
            oit = OrderItemTopping(order_item_id=oi.id, topping_id=tp_data.topping_id)
            db.add(oit)

    order.total = total
    db.commit()

    db.refresh(order)
    order_data = build_order_out(order)

    # Broadcast to WebSocket clients
    asyncio.create_task(manager.broadcast({"event": "order_created", "order": order_data}))

    # Notify Telegram
    try:
        from telegram_bot import notify_new_order
        asyncio.create_task(notify_new_order(order_data, db))
    except Exception:
        pass

    return order_data


@router.get("/orders")
def get_orders(db: Session = Depends(get_db)):
    orders = (
        db.query(Order)
        .options(
            joinedload(Order.table),
            joinedload(Order.items).joinedload(OrderItem.menu_item),
            joinedload(Order.items).joinedload(OrderItem.toppings).joinedload(OrderItemTopping.topping),
        )
        .filter(Order.status.in_(["pending", "serving", "done"]))
        .order_by(Order.created_at.desc())
        .all()
    )
    return [build_order_out(o) for o in orders]


@router.get("/orders/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = (
        db.query(Order)
        .options(
            joinedload(Order.table),
            joinedload(Order.items).joinedload(OrderItem.menu_item),
            joinedload(Order.items).joinedload(OrderItem.toppings).joinedload(OrderItemTopping.topping),
        )
        .filter(Order.id == order_id)
        .first()
    )
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return build_order_out(order)


@router.patch("/orders/{order_id}/status")
async def update_order_status(order_id: int, payload: OrderStatusUpdate, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    valid_transitions = {
        "pending": ["serving", "cancelled"],
        "serving": ["done", "cancelled"],
        "done": [],
        "cancelled": [],
    }
    if payload.status not in valid_transitions.get(order.status, []):
        raise HTTPException(
            status_code=400,
            detail=f"Cannot transition from {order.status} to {payload.status}",
        )

    order.status = payload.status
    order.updated_at = datetime.now(timezone.utc)
    if payload.cancel_reason:
        order.cancel_reason = payload.cancel_reason
    db.commit()
    db.refresh(order)

    order_data = build_order_out(order)
    asyncio.create_task(manager.broadcast({"event": "order_updated", "order": order_data}))

    # Sync to telegram if there is a telegram_message_id
    if order.telegram_message_id:
        try:
            from telegram_bot import sync_telegram_message
            asyncio.create_task(sync_telegram_message(order_data, order.telegram_message_id))
        except Exception:
            pass

    return order_data


@router.delete("/orders/{order_id}")
async def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    db.delete(order)
    db.commit()
    
    asyncio.create_task(manager.broadcast({"event": "order_deleted", "order_id": order_id}))
    return {"success": True}
