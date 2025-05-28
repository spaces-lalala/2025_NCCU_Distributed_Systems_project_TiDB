from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from services.payment_service import simulate_payment
from models.order import Order
from schemas.order import OrderOut

router = APIRouter(prefix="/api/payments", tags=["Payments"])

@router.post("/simulate/{order_id}", response_model=OrderOut)
def simulate_order_payment(
    order_id: str,
    db: Session = Depends(get_db)
):
    return simulate_payment(order_id=order_id, db=db)
