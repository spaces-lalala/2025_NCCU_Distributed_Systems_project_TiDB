from sqlalchemy.orm import Session
from models.order import Order
from fastapi import HTTPException

def simulate_payment(order_id: str, db: Session):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.status != "pending":
        raise HTTPException(status_code=400, detail="Order already paid or cancelled")

    order.status = "paid"
    db.commit()
    db.refresh(order)
    return order
