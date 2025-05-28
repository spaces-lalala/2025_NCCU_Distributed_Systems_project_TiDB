from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from database import get_db
from TiDB_shopping_backend.models.order import Order, OrderItem, Product
from schemas import OrderBase, OrderCreationRequest, OrderItemBase
from dependencies import get_current_user_id
import uuid
from datetime import datetime
from sqlalchemy import select

router = APIRouter(prefix="/api/orders", tags=["orders"])

@router.post("/", response_model=OrderBase, status_code=status.HTTP_201_CREATED)
def create_order(
    order_data: OrderCreationRequest,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    order_id = str(uuid.uuid4())
    order_number = f"ORD-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{order_id[:8]}"
    
    # 計算 total amount (可驗證前端傳來的金額)
    total_amount = sum(item.price * item.quantity for item in order_data.items)
    
    new_order = Order(
        id=order_id,
        order_number=order_number,
        order_date=datetime.utcnow(),
        total_amount=total_amount,
        status="PENDING",
        user_id=current_user_id
    )
    db.add(new_order)
    
    # 建立訂單項目 & 扣庫存
    for item in order_data.items:
        product = db.query(Product).filter(Product.id == item.productId).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.productId} not found")
        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Not enough stock for product {product.name}")
        
        product.stock -= item.quantity
        
        order_item = OrderItem(
            id=str(uuid.uuid4()),
            order_id=order_id,
            product_id=product.id,
            product_name=product.name,
            quantity=item.quantity,
            price=item.price
        )
        db.add(order_item)

    db.commit()
    db.refresh(new_order)

    return OrderBase(
        id=new_order.id,
        orderNumber=new_order.order_number,
        orderDate=new_order.order_date.isoformat(),
        totalAmount=new_order.total_amount,
        status=new_order.status,
        items=[
            OrderItemBase(
                productId=oi.product_id,
                productName=oi.product_name,
                quantity=oi.quantity,
                price=oi.price
            ) for oi in new_order.items
        ],
        userId=new_order.user_id
    )


@router.get("/", response_model=List[OrderBase])
def get_orders(
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    orders = db.query(Order).filter(Order.user_id == current_user_id).all()
    
    orders_response = []
    for order in orders:
        orders_response.append(OrderBase(
            id=order.id,
            orderNumber=order.order_number,
            orderDate=order.order_date.isoformat(),
            totalAmount=order.total_amount,
            status=order.status,
            items=[
                OrderItemBase(
                    productId=item.product_id,
                    productName=item.product_name,
                    quantity=item.quantity,
                    price=item.price
                ) for item in order.items
            ],
            userId=order.user_id
        ))
    return orders_response


@router.get("/{order_id}", response_model=OrderBase)
def get_order_detail(
    order_id: str,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order or order.user_id != current_user_id:
        raise HTTPException(status_code=404, detail="Order not found")

    return OrderBase(
        id=order.id,
        orderNumber=order.order_number,
        orderDate=order.order_date.isoformat(),
        totalAmount=order.total_amount,
        status=order.status,
        items=[
            OrderItemBase(
                productId=item.product_id,
                productName=item.product_name,
                quantity=item.quantity,
                price=item.price
            ) for item in order.items
        ],
        userId=order.user_id
    )

@router.post("/{order_id}/cancel", response_model=OrderBase)
def cancel_order_route(
    order_id: str,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    from services.order_service import cancel_order
    order = cancel_order(db, current_user_id, order_id)
    return order

@router.patch("/{order_id}/status")
def update_order_status_route(
    order_id: str,
    status: str,
    db: Session = Depends(get_db)
):
    from services.order_service import update_order_status
    order = update_order_status(db, order_id, status)
    return {"message": f"Order {order_id} updated to {status}"}


@router.get("/status/{status}", response_model=List[OrderBase])
def get_orders_by_status(
    status: str,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    orders = db.query(Order).filter(Order.user_id == current_user_id, Order.status == status).all()
    return [
        OrderBase(
            id=order.id,
            orderNumber=order.order_number,
            orderDate=order.order_date.isoformat(),
            totalAmount=order.total_amount,
            status=order.status,
            items=[
                OrderItemBase(
                    productId=item.product_id,
                    productName=item.product_name,
                    quantity=item.quantity,
                    price=item.price
                ) for item in order.items
            ],
            userId=order.user_id
        )
        for order in orders
    ]

@router.delete("/{order_id}")
def delete_order(
    order_id: str,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.status not in ["CANCELLED", "COMPLETED"]:
        raise HTTPException(status_code=400, detail="Can only delete cancelled or completed orders")
    
    db.delete(order)
    db.commit()
    return {"message": f"Order {order_id} deleted successfully"}
