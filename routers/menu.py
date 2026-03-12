from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Category, MenuItem, SpiceLevel, Topping
from schemas import CategoryOut, SpiceLevelOut, ToppingOut

router = APIRouter(prefix="/api", tags=["menu"])


@router.get("/categories", response_model=list[CategoryOut])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).order_by(Category.sort_order).all()


@router.get("/menu", response_model=list[CategoryOut])
def get_menu(db: Session = Depends(get_db)):
    cats = db.query(Category).order_by(Category.sort_order).all()
    return cats


@router.get("/spice-levels", response_model=list[SpiceLevelOut])
def get_spice_levels(db: Session = Depends(get_db)):
    return db.query(SpiceLevel).order_by(SpiceLevel.sort_order).all()


@router.get("/toppings", response_model=list[ToppingOut])
def get_toppings(db: Session = Depends(get_db)):
    return db.query(Topping).filter(Topping.available == True).all()
