from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from database import get_db
from models import Order, OrderItem, Product
from schemas import OrderOut, OrderCreationRequest, OrderItemBase
from schemas.order import OrderOut
from schemas.order_item import OrderItemOut
import uuid
from datetime import datetime
from sqlalchemy import select
from dependencies.auth import get_current_user_id

router = APIRouter(prefix="/api", tags=["orders"])

@router.post("/orders", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def create_order(
    order_data: OrderCreationRequest,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    order_id = str(uuid.uuid4())
    order_number = f"ORD-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{order_id[:8]}"
    
    # 計算 total amount - 從數據庫獲取實際價格
    total_amount = 0
    for item in order_data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Not enough stock for product {product.name}")
        total_amount += product.price * item.quantity
    
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
        product = db.query(Product).filter(Product.id == item.product_id).first()
        # 產品存在性和庫存已在上面檢查過，但我們需要再次獲取以更新庫存
        
        product.stock -= item.quantity
        if product.stock < 500:
            product.price+=10
        
        # 🔥 HTAP 相容：可選的即時更新 sold 欄位（展示即時性）
        # 注意：真正的 HTAP 不應該依賴這個欄位，而是即時從訂單計算
        product.sold = (product.sold or 0) + item.quantity
        
        order_item = OrderItem(
            id=str(uuid.uuid4()),
            order_id=order_id,
            product_id=product.id,
            product_name=product.name,
            quantity=item.quantity,
            price=product.price  # 使用從數據庫獲取的價格
        )
        db.add(order_item)

    # 🚀 HTAP 展示：印出即時分析訊息
    print(f"📦 訂單 {order_number} 已創建，TiDB HTAP 可即時分析最新銷售數據")

    db.commit()
    db.refresh(new_order)
    
    return OrderOut(
        id=new_order.id,
        order_number=new_order.order_number,
        order_date=new_order.order_date,
        total_amount=new_order.total_amount,
        status=new_order.status,
        user_id=new_order.user_id,
        items=[
            OrderItemOut(
                id=oi.id,
                product_id=oi.product_id,
                product_name=oi.product_name,
                quantity=oi.quantity,
                price=oi.price
            ) for oi in new_order.items
        ]
    )


@router.get("/orders", response_model=List[OrderOut])
def get_orders(
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    orders = db.query(Order).filter(Order.user_id == current_user_id).all()
    
    orders_response = []
    for order in orders:
        orders_response.append(OrderOut(
            id=order.id,
            order_number=order.order_number,
            order_date=order.order_date,
            total_amount=order.total_amount,
            status=order.status,
            user_id=order.user_id,
            items=[
                OrderItemOut(
                    id=item.id,
                    product_id=item.product_id,
                    product_name=item.product_name,
                    quantity=item.quantity,
                    price=item.price
                ) for item in order.items
            ]
        ))
    return orders_response


@router.get("/orders/{order_id}", response_model=OrderOut)
def get_order_detail(
    order_id: str,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order or order.user_id != current_user_id:
        raise HTTPException(status_code=404, detail="Order not found")

    return OrderOut(
        id=order.id,
        order_number=order.order_number,
        order_date=order.order_date,
        total_amount=order.total_amount,
        status=order.status,
        user_id=order.user_id,
        items=[
            OrderItemOut(
                id=item.id,
                product_id=item.product_id,
                product_name=item.product_name,
                quantity=item.quantity,
                price=item.price
            ) for item in order.items
        ]
    )

@router.post("/orders/{order_id}/cancel", response_model=OrderOut)
def cancel_order_route(
    order_id: str,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    from services.order_service import cancel_order
    order = cancel_order(db, current_user_id, order_id)
    return OrderOut.from_orm(order)

@router.patch("/orders/{order_id}/status")
def update_order_status_route(
    order_id: str,
    status: str,
    db: Session = Depends(get_db)
):
    from services.order_service import update_order_status
    order = update_order_status(db, order_id, status)
    return {"message": f"Order {order_id} updated to {status}"}
