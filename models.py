from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base


def utcnow():
    return datetime.now(timezone.utc)


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name_th = Column(String, nullable=False)
    name_en = Column(String, nullable=False)
    name_zh = Column(String, nullable=False)
    icon = Column(String, default="🍲")
    sort_order = Column(Integer, default=0)
    items = relationship("MenuItem", back_populates="category")


class MenuItem(Base):
    __tablename__ = "menu_items"
    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    name_th = Column(String, nullable=False)
    name_en = Column(String, nullable=False)
    name_zh = Column(String, nullable=False)
    description_th = Column(Text, default="")
    description_en = Column(Text, default="")
    description_zh = Column(Text, default="")
    price = Column(Float, nullable=False)
    image_url = Column(String, default="")
    available = Column(Boolean, default=True)
    category = relationship("Category", back_populates="items")
    order_items = relationship("OrderItem", back_populates="menu_item")


class SpiceLevel(Base):
    __tablename__ = "spice_levels"
    id = Column(Integer, primary_key=True, index=True)
    name_th = Column(String, nullable=False)
    name_en = Column(String, nullable=False)
    name_zh = Column(String, nullable=False)
    extra_price = Column(Float, default=0.0)
    sort_order = Column(Integer, default=0)


class Topping(Base):
    __tablename__ = "toppings"
    id = Column(Integer, primary_key=True, index=True)
    name_th = Column(String, nullable=False)
    name_en = Column(String, nullable=False)
    name_zh = Column(String, nullable=False)
    price = Column(Float, default=0.0)
    available = Column(Boolean, default=True)


class TableInfo(Base):
    __tablename__ = "tables"
    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, unique=True, nullable=False)
    name = Column(String, default="")
    orders = relationship("Order", back_populates="table")


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    table_id = Column(Integer, ForeignKey("tables.id"))
    status = Column(String, default="pending")  # pending | serving | done | cancelled
    total = Column(Float, default=0.0)
    cancel_reason = Column(String, default="")
    telegram_message_id = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utcnow)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)
    table = relationship("TableInfo", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"))
    spice_level_id = Column(Integer, ForeignKey("spice_levels.id"), nullable=True)
    quantity = Column(Integer, default=1)
    unit_price = Column(Float, default=0.0)
    notes = Column(Text, default="")
    order = relationship("Order", back_populates="items")
    menu_item = relationship("MenuItem", back_populates="order_items")
    toppings = relationship("OrderItemTopping", back_populates="order_item", cascade="all, delete-orphan")


class OrderItemTopping(Base):
    __tablename__ = "order_item_toppings"
    id = Column(Integer, primary_key=True, index=True)
    order_item_id = Column(Integer, ForeignKey("order_items.id"))
    topping_id = Column(Integer, ForeignKey("toppings.id"))
    order_item = relationship("OrderItem", back_populates="toppings")
    topping = relationship("Topping")
