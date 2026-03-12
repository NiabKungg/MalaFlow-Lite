from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# ─── Topping ────────────────────────────────────────────────────────────────

class ToppingOut(BaseModel):
    id: int
    name_th: str
    name_en: str
    name_zh: str
    price: float

    class Config:
        from_attributes = True


# ─── Spice Level ─────────────────────────────────────────────────────────────

class SpiceLevelOut(BaseModel):
    id: int
    name_th: str
    name_en: str
    name_zh: str
    extra_price: float
    sort_order: int

    class Config:
        from_attributes = True


# ─── Menu ───────────────────────────────────────────────────────────────────

class MenuItemOut(BaseModel):
    id: int
    category_id: int
    name_th: str
    name_en: str
    name_zh: str
    description_th: str
    description_en: str
    description_zh: str
    price: float
    image_url: str
    available: bool

    class Config:
        from_attributes = True


class CategoryOut(BaseModel):
    id: int
    name_th: str
    name_en: str
    name_zh: str
    icon: str
    sort_order: int
    items: List[MenuItemOut] = []

    class Config:
        from_attributes = True


# ─── Table ───────────────────────────────────────────────────────────────────

class TableOut(BaseModel):
    id: int
    number: int
    name: str

    class Config:
        from_attributes = True


# ─── Order ───────────────────────────────────────────────────────────────────

class OrderItemToppingCreate(BaseModel):
    topping_id: int


class OrderItemCreate(BaseModel):
    menu_item_id: int
    spice_level_id: Optional[int] = None
    quantity: int = 1
    notes: str = ""
    toppings: List[OrderItemToppingCreate] = []


class OrderCreate(BaseModel):
    table_id: int
    items: List[OrderItemCreate]


class OrderStatusUpdate(BaseModel):
    status: str
    cancel_reason: Optional[str] = ""


class ToppingSnap(BaseModel):
    id: int
    name_th: str
    name_en: str
    name_zh: str
    price: float

    class Config:
        from_attributes = True


class OrderItemOut(BaseModel):
    id: int
    menu_item_id: int
    menu_item_name_th: str = ""
    menu_item_name_en: str = ""
    menu_item_name_zh: str = ""
    menu_item_image_url: str = ""
    spice_level_id: Optional[int]
    spice_level_name_th: str = ""
    spice_level_name_en: str = ""
    quantity: int
    unit_price: float
    notes: str
    toppings: List[ToppingSnap] = []

    class Config:
        from_attributes = True


class OrderOut(BaseModel):
    id: int
    table_id: int
    table_number: int = 0
    status: str
    total: float
    cancel_reason: str
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemOut] = []

    class Config:
        from_attributes = True


# ─── Auth ────────────────────────────────────────────────────────────────────

class PinVerify(BaseModel):
    pin: str


# ─── Summary ─────────────────────────────────────────────────────────────────

class DailySummary(BaseModel):
    date: str
    total_revenue: float
    order_count: int
    cancelled_count: int
    avg_service_minutes: float
