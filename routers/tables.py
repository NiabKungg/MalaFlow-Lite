from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import TableInfo
from schemas import TableOut

router = APIRouter(prefix="/api", tags=["tables"])


@router.get("/tables", response_model=list[TableOut])
def get_tables(db: Session = Depends(get_db)):
    return db.query(TableInfo).order_by(TableInfo.number).all()
