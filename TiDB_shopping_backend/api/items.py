from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Item  # 你實際的 model 名稱

router = APIRouter()

@router.get("/items")
def read_items(db: Session = Depends(get_db)):
    items = db.query(Item).all()
    return items
