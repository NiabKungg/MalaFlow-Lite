from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models import Order, OrderItem
from datetime import datetime, timedelta, timezone
from schemas import DailySummary

router = APIRouter(prefix="/api", tags=["history"])


@router.get("/history")
def get_history(days: int = 30, db: Session = Depends(get_db)):
    since = datetime.now(timezone.utc) - timedelta(days=days)
    orders = (
        db.query(Order)
        .filter(Order.created_at >= since)
        .filter(Order.status.in_(["done", "cancelled"]))
        .order_by(Order.created_at.desc())
        .all()
    )
    result = []
    for o in orders:
        result.append({
            "id": o.id,
            "table_id": o.table_id,
            "table_number": o.table.number if o.table else 0,
            "status": o.status,
            "total": o.total,
            "cancel_reason": o.cancel_reason or "",
            "created_at": o.created_at.isoformat() if o.created_at else "",
            "updated_at": o.updated_at.isoformat() if o.updated_at else "",
            "items": [
                {
                    "id": oi.id,
                    "menu_item_name_th": oi.menu_item.name_th if oi.menu_item else "",
                    "menu_item_name_en": oi.menu_item.name_en if oi.menu_item else "",
                    "quantity": oi.quantity,
                    "unit_price": oi.unit_price,
                }
                for oi in o.items
            ],
        })
    return result


@router.get("/summary")
def get_daily_summary(date: str = Query(default=None), db: Session = Depends(get_db)):
    if date:
        try:
            target = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            target = datetime.now(timezone.utc)
    else:
        target = datetime.now(timezone.utc)

    day_start = target.replace(hour=0, minute=0, second=0, microsecond=0)
    day_end = day_start + timedelta(days=1)

    orders = (
        db.query(Order)
        .filter(Order.created_at >= day_start, Order.created_at < day_end)
        .all()
    )

    done_orders = [o for o in orders if o.status == "done"]
    cancelled_orders = [o for o in orders if o.status == "cancelled"]
    total_revenue = sum(o.total for o in done_orders)

    service_times = []
    for o in done_orders:
        if o.created_at and o.updated_at:
            delta = (o.updated_at - o.created_at).total_seconds() / 60
            service_times.append(delta)

    avg_service = sum(service_times) / len(service_times) if service_times else 0.0

    return {
        "date": target.strftime("%Y-%m-%d"),
        "total_revenue": total_revenue,
        "order_count": len(done_orders),
        "cancelled_count": len(cancelled_orders),
        "avg_service_minutes": round(avg_service, 1),
    }
