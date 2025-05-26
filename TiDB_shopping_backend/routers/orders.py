from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from models import Order, OrderItem, Product
from schemas import OrderBase, OrderCreationRequest
from dependencies import get_current_user_id
import uuid
from datetime import datetime

router = APIRouter(prefix="/api/orders", tags=["orders"])

@router.post("/", response_model=OrderBase, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: OrderCreationRequest,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    # 事務處理，減少庫存，建立訂單 + 明細
    async with session.begin():  # 事務開始
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
        session.add(new_order)
        
        # 建立訂單項目 & 扣庫存
        for item in order_data.items:
            product = await session.get(Product, item.productId)
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
            session.add(order_item)
        
        # Commit 在 async with 區塊結束會自動做
    await session.commit()
    
    # 查詢剛建立的訂單及明細並回傳（或自己組裝）
    created_order = await session.get(Order, order_id)
    await session.refresh(created_order)
    # 這裡要根據你的 Pydantic model 組裝 items，通常用 ORM model 轉 Pydantic

    # 簡化回傳，實務可做更多
    return OrderBase(
        id=created_order.id,
        orderNumber=created_order.order_number,
        orderDate=created_order.order_date.isoformat(),
        totalAmount=created_order.total_amount,
        status=created_order.status,
        items=[OrderItemBase(
            productId=oi.product_id,
            productName=oi.product_name,
            quantity=oi.quantity,
            price=oi.price
        ) for oi in created_order.items],
        userId=created_order.user_id
    )


@router.get("/", response_model=List[OrderBase])
async def get_orders(
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    # 查詢該用戶所有訂單
    result = await session.execute(
        select(Order).where(Order.user_id == current_user_id)
    )
    orders = result.scalars().all()

    # 取明細 (如果 ORM 有設定 relationship，使用 .items)
    orders_response = []
    for order in orders:
        await session.refresh(order)
        orders_response.append(OrderBase(
            id=order.id,
            orderNumber=order.order_number,
            orderDate=order.order_date.isoformat(),
            totalAmount=order.total_amount,
            status=order.status,
            items=[OrderItemBase(
                productId=item.product_id,
                productName=item.product_name,
                quantity=item.quantity,
                price=item.price
            ) for item in order.items],
            userId=order.user_id
        ))
    return orders_response


@router.get("/{order_id}", response_model=OrderBase)
async def get_order_detail(
    order_id: str,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    order = await session.get(Order, order_id)
    if not order or order.user_id != current_user_id:
        raise HTTPException(status_code=404, detail="Order not found")
    await session.refresh(order)
    return OrderBase(
        id=order.id,
        orderNumber=order.order_number,
        orderDate=order.order_date.isoformat(),
        totalAmount=order.total_amount,
        status=order.status,
        items=[OrderItemBase(
            productId=item.product_id,
            productName=item.product_name,
            quantity=item.quantity,
            price=item.price
        ) for item in order.items],
        userId=order.user_id
    )
