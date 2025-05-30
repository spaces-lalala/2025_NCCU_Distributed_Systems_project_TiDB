from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.product import Product
from models.order import Order
from models.order_item import OrderItem
import uuid
from datetime import datetime

def create_order(db: Session, user_id: str, items: list):
    order_id = str(uuid.uuid4())
    order_number = f"ORD-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{order_id[:8]}"
    
    total_amount = 0
    # 1. 檢查庫存和計算總價
    for item in items:
        product = db.query(Product).filter(Product.id == item['product_id']).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item['product_id']} not found")
        if product.stock < item['quantity']:
            raise HTTPException(status_code=400, detail=f"Product {product.name} stock insufficient")
        total_amount += product.price * item['quantity']
    
    # 2. 建立訂單
    new_order = Order(
        id=order_id,
        order_number=order_number,
        order_date=datetime.utcnow(),
        total_amount=total_amount,
        status="PENDING",
        user_id=user_id
    )
    db.add(new_order)
    
    # 3. 建立訂單明細與扣庫存
    for item in items:
        product = db.query(Product).filter(Product.id == item['product_id']).first()
        product.stock -= item['quantity']

        order_item = OrderItem(
            id=str(uuid.uuid4()),
            order_id=order_id,
            product_id=product.id,
            product_name=product.name,
            quantity=item['quantity'],
            price=product.price
        )
        db.add(order_item)
    db.commit()
    db.refresh(new_order)
    return new_order

def cancel_order(db: Session, user_id: str, order_id: str):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == user_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.status != "PENDING":
        raise HTTPException(status_code=400, detail="Cannot cancel a non-pending order")

    # 恢復庫存
    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        product.stock += item.quantity

    order.status = "CANCELLED"
    db.commit()
    return order

def update_order_status(db: Session, order_id: str, new_status: str):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = new_status
    db.commit()
    return order
