"""
MalaFlow POS - Seed Data Script
Run this once to populate the database with initial menu data.
Usage: python seed_data.py
"""
from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

def seed():
    # Clear existing data
    db.query(models.OrderItemTopping).delete()
    db.query(models.OrderItem).delete()
    db.query(models.Order).delete()
    db.query(models.Topping).delete()
    db.query(models.SpiceLevel).delete()
    db.query(models.MenuItem).delete()
    db.query(models.Category).delete()
    db.query(models.TableInfo).delete()
    db.commit()

    # ─── Tables ───────────────────────────────────────────────────────────────
    tables = []
    for i in range(1, 31):
        tables.append(models.TableInfo(number=i, name=f"โต๊ะ {i}"))
    db.add_all(tables)

    # ─── Spice Levels ─────────────────────────────────────────────────────────
    spice_levels = [
        models.SpiceLevel(name_th="ไม่เผ็ด", name_en="No Spice", name_zh="不辣", extra_price=0, sort_order=0),
        models.SpiceLevel(name_th="เผ็ดน้อย", name_en="Mild", name_zh="微辣", extra_price=0, sort_order=1),
        models.SpiceLevel(name_th="เผ็ดกลาง", name_en="Medium", name_zh="中辣", extra_price=0, sort_order=2),
        models.SpiceLevel(name_th="เผ็ดมาก", name_en="Hot", name_zh="大辣", extra_price=10, sort_order=3),
        models.SpiceLevel(name_th="เผ็ดพิเศษ", name_en="Extra Hot", name_zh="特辣", extra_price=20, sort_order=4),
    ]
    db.add_all(spice_levels)

    # ─── Toppings ─────────────────────────────────────────────────────────────
    toppings = [
        models.Topping(name_th="ชีส", name_en="Cheese", name_zh="芝士", price=20),
        models.Topping(name_th="ไข่ไก่", name_en="Egg", name_zh="鸡蛋", price=10),
        models.Topping(name_th="ลูกชิ้นเพิ่ม", name_en="Extra Meatball", name_zh="加肉丸", price=15),
        models.Topping(name_th="ผักรวม", name_en="Mixed Vegetables", name_zh="素菜", price=10),
        models.Topping(name_th="เห็ดรวม", name_en="Mixed Mushrooms", name_zh="杂菇", price=20),
        models.Topping(name_th="บะหมี่", name_en="Noodles", name_zh="面条", price=10),
        models.Topping(name_th="กุ้งเพิ่ม", name_en="Extra Shrimp", name_zh="加虾", price=30),
        models.Topping(name_th="เต้าหู้", name_en="Tofu", name_zh="豆腐", price=10),
    ]
    db.add_all(toppings)
    db.commit()

    # ─── Categories & Menu Items ──────────────────────────────────────────────
    cat_mala = models.Category(name_th="หม่าล่า", name_en="Mala", name_zh="麻辣", icon="🌶️", sort_order=1)
    cat_shabu = models.Category(name_th="ชาบู", name_en="Shabu", name_zh="涮涮锅", icon="🍲", sort_order=2)
    cat_protein = models.Category(name_th="เนื้อสัตว์", name_en="Protein", name_zh="肉类", icon="🥩", sort_order=3)
    cat_veg = models.Category(name_th="ผักและเต้าหู้", name_en="Vegetables & Tofu", name_zh="蔬菜豆腐", icon="🥬", sort_order=4)
    cat_noodles = models.Category(name_th="เส้น", name_en="Noodles", name_zh="面食", icon="🍜", sort_order=5)
    cat_drinks = models.Category(name_th="เครื่องดื่ม", name_en="Drinks", name_zh="饮料", icon="🥤", sort_order=6)
    db.add_all([cat_mala, cat_shabu, cat_protein, cat_veg, cat_noodles, cat_drinks])
    db.commit()

    menu_items = [
        # หม่าล่า
        models.MenuItem(category_id=cat_mala.id, name_th="หม่าล่าน้ำแดง", name_en="Red Mala Broth", name_zh="红汤麻辣锅底",
                        description_th="น้ำซุปหม่าล่าสูตรต้นตำรับ เผ็ดจัดจ้าน", description_en="Classic spicy mala broth", description_zh="经典麻辣红汤",
                        price=89, image_url="/img/image-test-01.png"),
        models.MenuItem(category_id=cat_mala.id, name_th="หม่าล่าน้ำขาว", name_en="Mild Mala Broth", name_zh="白汤麻辣锅底",
                        description_th="น้ำซุปหม่าล่าแบบอ่อน เหมาะสำหรับผู้ที่ไม่ชอบเผ็ดมาก", description_en="Mild mala broth for light spice lovers", description_zh="清淡麻辣底汤",
                        price=79, image_url="/img/image-test-02.png"),
        models.MenuItem(category_id=cat_mala.id, name_th="หม่าล่าสองรส", name_en="Dual Mala Broth", name_zh="鸳鸯锅底",
                        description_th="แบ่งครึ่งระหว่างน้ำแดง-น้ำขาว", description_en="Half red, half mild broth", description_zh="一锅两味",
                        price=99, image_url=""),
        # ชาบู
        models.MenuItem(category_id=cat_shabu.id, name_th="ชาบูน้ำสุกี้", name_en="Sukiyaki Shabu", name_zh="寿喜烧锅底",
                        description_th="น้ำซุปชาบูแบบญี่ปุ่น หวานนิดๆ", description_en="Japanese-style sweet shabu broth", description_zh="日式涮涮锅",
                        price=79, image_url=""),
        models.MenuItem(category_id=cat_shabu.id, name_th="ชาบูน้ำกระดูก", name_en="Bone Broth Shabu", name_zh="骨汤锅底",
                        description_th="น้ำซุปกระดูกใสหอม ต้มนาน 24 ชั่วโมง", description_en="Clear bone broth simmered 24 hrs", description_zh="24小时骨汤",
                        price=89, image_url=""),
        # เนื้อสัตว์
        models.MenuItem(category_id=cat_protein.id, name_th="เนื้อวัวหั่น", name_en="Sliced Beef", name_zh="牛肉片",
                        description_th="เนื้อวัวแช่แข็งหั่นบาง", description_en="Thinly sliced frozen beef", description_zh="薄切冻牛肉",
                        price=129, image_url=""),
        models.MenuItem(category_id=cat_protein.id, name_th="หมูสามชั้น", name_en="Pork Belly", name_zh="五花肉",
                        description_th="หมูสามชั้นหั่นบาง", description_en="Thinly sliced pork belly", description_zh="薄切五花肉",
                        price=99, image_url=""),
        models.MenuItem(category_id=cat_protein.id, name_th="กุ้งแม่น้ำ", name_en="River Shrimp", name_zh="河虾",
                        description_th="กุ้งแม่น้ำสดขนาดกลาง 5 ตัว", description_en="Fresh river shrimp, 5 pcs", description_zh="新鲜河虾5只",
                        price=149, image_url=""),
        models.MenuItem(category_id=cat_protein.id, name_th="ปลาหมึก", name_en="Squid", name_zh="鱿鱼",
                        description_th="ปลาหมึกสดหั่นชิ้น", description_en="Fresh sliced squid", description_zh="新鲜鱿鱼",
                        price=119, image_url=""),
        models.MenuItem(category_id=cat_protein.id, name_th="ลูกชิ้นรวม", name_en="Mixed Meatballs", name_zh="混合肉丸",
                        description_th="ลูกชิ้นเนื้อ หมู และปลา", description_en="Beef, pork & fish meatballs", description_zh="牛猪鱼丸拼盘",
                        price=79, image_url=""),
        models.MenuItem(category_id=cat_protein.id, name_th="ไก่บ้านสับ", name_en="Minced Chicken", name_zh="碎鸡肉",
                        description_th="ไก่บ้านสดสับพร้อมลวก", description_en="Fresh minced chicken", description_zh="新鲜碎鸡肉",
                        price=89, image_url=""),
        # ผัก
        models.MenuItem(category_id=cat_veg.id, name_th="ผักรวม", name_en="Mixed Vegetables", name_zh="素菜拼盘",
                        description_th="ผักรวมหลากชนิด", description_en="Assorted fresh vegetables", description_zh="时令蔬菜拼盘",
                        price=49, image_url=""),
        models.MenuItem(category_id=cat_veg.id, name_th="เห็ดรวม", name_en="Mixed Mushrooms", name_zh="杂菇拼盘",
                        description_th="เห็ดหอม เห็ดเข็มทอง เห็ดโคน", description_en="Shiitake, enoki, eryngii", description_zh="香菇金针菇杏鲍菇",
                        price=59, image_url=""),
        models.MenuItem(category_id=cat_veg.id, name_th="เต้าหู้รวม", name_en="Tofu Set", name_zh="豆腐拼盘",
                        description_th="เต้าหู้แข็ง เต้าหู้นิ่ม เต้าหู้ไข่", description_en="Firm, soft & egg tofu", description_zh="硬豆腐嫩豆腐蛋豆腐",
                        price=49, image_url=""),
        # เส้น
        models.MenuItem(category_id=cat_noodles.id, name_th="วุ้นเส้น", name_en="Glass Noodles", name_zh="粉丝",
                        description_th="วุ้นเส้นแก้ว", description_en="Transparent glass noodles", description_zh="透明粉丝",
                        price=29, image_url=""),
        models.MenuItem(category_id=cat_noodles.id, name_th="บะหมี่รัง", name_en="Egg Noodles", name_zh="鸡蛋面",
                        description_th="บะหมี่ไข่ทรงกลม", description_en="Nest-style egg noodles", description_zh="鸟巢鸡蛋面",
                        price=29, image_url=""),
        models.MenuItem(category_id=cat_noodles.id, name_th="ข้าว", name_en="Steamed Rice", name_zh="米饭",
                        description_th="ข้าวสวยหอมมะลิ", description_en="Steamed jasmine rice", description_zh="茉莉香米饭",
                        price=15, image_url=""),
        # เครื่องดื่ม
        models.MenuItem(category_id=cat_drinks.id, name_th="น้ำเปล่า", name_en="Mineral Water", name_zh="矿泉水",
                        description_th="น้ำดื่มบรรจุขวด 600ml", description_en="Bottled water 600ml", description_zh="瓶装水600ml",
                        price=15, image_url=""),
        models.MenuItem(category_id=cat_drinks.id, name_th="น้ำอัดลม", name_en="Soft Drink", name_zh="汽水",
                        description_th="โค้ก สไปรต์ หรือเป๊ปซี่", description_en="Coke, Sprite or Pepsi", description_zh="可口可乐/雪碧/百事",
                        price=25, image_url=""),
        models.MenuItem(category_id=cat_drinks.id, name_th="ชาเย็น", name_en="Thai Iced Tea", name_zh="泰式冰茶",
                        description_th="ชาไทยใส่นม", description_en="Thai milk tea with ice", description_zh="泰式奶茶加冰",
                        price=35, image_url=""),
        models.MenuItem(category_id=cat_drinks.id, name_th="เบียร์ช้าง", name_en="Chang Beer", name_zh="象牌啤酒",
                        description_th="เบียร์ช้างกระป๋อง 330ml", description_en="Chang beer can 330ml", description_zh="象牌啤酒330ml",
                        price=65, image_url=""),
        models.MenuItem(category_id=cat_drinks.id, name_th="น้ำผลไม้", name_en="Fruit Juice", name_zh="果汁",
                        description_th="น้ำส้ม มะพร้าว หรือสับปะรด", description_en="Orange, coconut or pineapple", description_zh="橙汁/椰子汁/菠萝汁",
                        price=45, image_url=""),
    ]
    db.add_all(menu_items)
    db.commit()
    print(f"✅ Seed data complete!")
    print(f"   📋 {len(tables)} tables")
    print(f"   🌶️ {len(spice_levels)} spice levels")
    print(f"   🍴 {len(toppings)} toppings")
    print(f"   🍽️ {len(menu_items)} menu items across 6 categories")

try:
    seed()
finally:
    db.close()
