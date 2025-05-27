from sqlalchemy.orm import Session
from sqlalchemy import func
from models.order_item import OrderItem
from models.product import Product
from models.order import Order

def get_bestsellers(db: Session, limit: int = 5):
    results = (
        db.query(
            Product,
            func.sum(OrderItem.quantity).label("total_sold")
        )
        .join(OrderItem, Product.id == OrderItem.product_id)
        .join(Order, Order.id == OrderItem.order_id)
        .filter(Order.status == "paid")
        .group_by(Product.id)
        .order_by(func.sum(OrderItem.quantity).desc())
        .limit(limit)
        .all()
    )

    return [product for product, _ in results]
