from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from models.product import Product
from models import Category
from schemas.product import ProductOut, ProductDetailOut, ErrorDetail

router = APIRouter(prefix="/api", tags=["products"])

@router.get("/products", response_model=List[ProductOut])
def list_products(
    skip: int = 0,
    limit: int = 10,
    category: Optional[str] = None,
    sort_by: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Product)

    # 篩選分類
    if category:
        cat = db.query(Category).filter(Category.name == category).first()
        if cat:
            query = query.filter(Product.category_name == cat.name)
        else:
            return []

    # 排序
    if sort_by == "price_asc":
        query = query.order_by(Product.price.asc())
    elif sort_by == "price_desc":
        query = query.order_by(Product.price.desc())
    elif sort_by == "name_asc":
        query = query.order_by(Product.name.asc())

    products = query.offset(skip).limit(limit).all()
    return products

@router.get("/products/bestsellers", response_model=List[ProductOut])
def read_best_sellers(limit: int = 5, db: Session = Depends(get_db)):
    """
    🔥 TiDB HTAP 展示：熱銷排行榜即時分析
    完全不依賴過時的 sold 欄位，直接從最新交易數據即時計算真實銷量
    這展現了 TiDB HTAP 的核心價值：無需 ETL，即時分析最新業務數據
    """
    from sqlalchemy import func, distinct, case
    from models.order_item import OrderItem
    from models.order import Order
    
    try:
        # 🚀 純 HTAP 查詢：即時從訂單表分析真實銷量
        htap_query = (
            db.query(
                Product,
                func.coalesce(func.sum(
                    case(
                        (Order.status.in_(["PENDING", "paid", "shipped", "delivered"]), OrderItem.quantity),
                        else_=0
                    )
                ), 0).label("real_sales"),
                func.count(distinct(Order.id)).label("order_count"),
                func.max(Order.order_date).label("last_sold_date"),
                func.sum(
                    case(
                        (Order.status.in_(["PENDING", "paid", "shipped", "delivered"]), 
                         OrderItem.quantity * OrderItem.price),
                        else_=0
                    )
                ).label("total_revenue")
            )
            .outerjoin(OrderItem, Product.id == OrderItem.product_id)
            .outerjoin(Order, Order.id == OrderItem.order_id)
            .group_by(Product.id, Product.name, Product.price, Product.stock, Product.sold, Product.image_url, Product.category_name)
            .order_by(func.coalesce(func.sum(
                case(
                    (Order.status.in_(["PENDING", "paid", "shipped", "delivered"]), OrderItem.quantity),
                    else_=0
                )
            ), 0).desc())
            .limit(limit)
        )
        
        results = htap_query.all()
        
        # 展示 HTAP 分析結果
        print(f"🔥 TiDB HTAP 即時分析結果：")
        products = []
        for product, real_sales, order_count, last_sold, total_revenue in results:
            print(f"   📊 {product.name}: 實際銷量 {real_sales} (vs 舊sold欄位 {product.sold})")
            
            # 動態更新產品的銷量顯示（不修改資料庫，純粹為了展示）
            product.sold = int(real_sales) if real_sales else 0
            products.append(product)
        
        if any(p.sold > 0 for p in products):
            print(f"✨ 成功使用 HTAP 分析了 {len([p for p in products if p.sold > 0])} 個有銷量的商品")
        else:
            print("📝 目前沒有有效訂單數據，顯示所有商品（銷量為0）")
            
        return products
        
    except Exception as e:
        print(f"⚠️ HTAP 查詢異常: {e}")
        # 極簡備用方案
        products = db.query(Product).limit(limit).all()
        for product in products:
            product.sold = 0  # 重置為0，表示無法計算真實銷量
        return products

@router.get("/analytics/sales-trends")
def get_sales_trends(days: int = 7, db: Session = Depends(get_db)):
    """
    📊 TiDB HTAP 展示：銷售趨勢即時分析
    展示指定天數內的銷售趨勢，展現 HTAP 的即時分析能力
    """
    from sqlalchemy import func, text
    from datetime import datetime, timedelta
    from models.order import Order
    
    try:
        cutoff_date = datetime.now() - timedelta(days=days)
        
        trends = (
            db.query(
                func.date(Order.order_date).label("sale_date"),
                func.count(Order.id).label("orders_count"),
                func.sum(Order.total_amount).label("revenue"),
                func.avg(Order.total_amount).label("avg_order_value")
            )
            .filter(Order.order_date >= cutoff_date)
            .filter(Order.status.in_(["paid", "shipped", "delivered"]))
            .group_by(func.date(Order.order_date))
            .order_by("sale_date")
            .all()
        )
        
        return {
            "status": "success",
            "message": f"TiDB HTAP: 即時分析了最近 {days} 天的銷售趨勢",
            "data": [
                {
                    "date": trend.sale_date.isoformat() if trend.sale_date else None,
                    "orders": trend.orders_count,
                    "revenue": float(trend.revenue or 0),
                    "avg_order_value": float(trend.avg_order_value or 0)
                }
                for trend in trends
            ]
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"HTAP 分析失敗: {str(e)}",
            "data": []
        }

@router.get("/analytics/product-performance")
def get_product_performance(limit: int = 10, db: Session = Depends(get_db)):
    """
    🎯 TiDB HTAP 展示：產品效能即時分析
    多維度分析產品銷售表現，展現複雜 OLAP 查詢能力
    """
    from sqlalchemy import func, distinct
    from models.order_item import OrderItem
    from models.order import Order
    
    try:
        performance = (
            db.query(
                Product.name,
                Product.price,
                func.sum(OrderItem.quantity).label("total_sold"),
                func.sum(OrderItem.quantity * OrderItem.price).label("total_revenue"),
                func.count(distinct(Order.user_id)).label("unique_customers"),
                func.count(distinct(Order.id)).label("order_count")
            )
            .join(OrderItem, Product.id == OrderItem.product_id)
            .join(Order, Order.id == OrderItem.order_id)
            .filter(Order.status.in_(["paid", "shipped", "delivered"]))
            .group_by(Product.id, Product.name, Product.price)
            .order_by(func.sum(OrderItem.quantity * OrderItem.price).desc())
            .limit(limit)
            .all()
        )
        
        return {
            "status": "success", 
            "message": f"TiDB HTAP: 即時分析了 {len(performance)} 個產品的多維度效能",
            "data": [
                {
                    "product": perf.name,
                    "price": float(perf.price),
                    "units_sold": perf.total_sold,
                    "revenue": float(perf.total_revenue),
                    "unique_customers": perf.unique_customers,
                    "order_count": perf.order_count,
                    "revenue_per_customer": float(perf.total_revenue / perf.unique_customers) if perf.unique_customers > 0 else 0
                }
                for perf in performance
            ]
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"HTAP 分析失敗: {str(e)}",
            "data": []
        }

@router.get("/products/{product_id}", response_model=ProductDetailOut, responses={404: {"model": ErrorDetail}})
def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    Fetch product details, including description, from the database.
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # 返回產品詳細資訊，包括 description
    return ProductDetailOut(
        id=product.id,
        name=product.name,
        description=product.description,
        price=product.price,
        image_url=product.image_url,
        sold=product.sold,
        stock=product.stock,
        category_name=product.category_name
    )

@router.get("/debug/htap-verification")
def verify_htap_functionality(db: Session = Depends(get_db)):
    """
    🔍 HTAP 驗證端點：檢查訂單數據與產品銷量的一致性
    用於驗證 HTAP 查詢是否正確工作
    """
    from sqlalchemy import func
    from models.order_item import OrderItem
    from models.order import Order
    
    try:
        # 1. 檢查訂單總數
        total_orders = db.query(func.count(Order.id)).scalar()
        
        # 2. 檢查訂單項目總數
        total_order_items = db.query(func.count(OrderItem.id)).scalar()
        
        # 3. 檢查各產品的實際銷量
        product_sales = (
            db.query(
                Product.name,
                Product.sold,
                func.coalesce(func.sum(OrderItem.quantity), 0).label("actual_sales")
            )
            .outerjoin(OrderItem, Product.id == OrderItem.product_id)
            .outerjoin(Order, Order.id == OrderItem.order_id)
            .group_by(Product.id, Product.name, Product.sold)
            .all()
        )
        
        # 4. 檢查訂單狀態分布
        order_status_count = (
            db.query(Order.status, func.count(Order.id).label("count"))
            .group_by(Order.status)
            .all()
        )
        
        return {
            "status": "success",
            "message": "TiDB HTAP 驗證完成",
            "data": {
                "total_orders": total_orders,
                "total_order_items": total_order_items,
                "product_sales": [
                    {
                        "product": sale.name,
                        "stored_sold": sale.sold,
                        "actual_sales": int(sale.actual_sales),
                        "consistent": sale.sold == int(sale.actual_sales)
                    }
                    for sale in product_sales
                ],
                "order_status_distribution": [
                    {"status": status.status, "count": status.count}
                    for status in order_status_count
                ]
            }
        }
        
    except Exception as e:
        return {
            "status": "error", 
            "message": f"HTAP 驗證失敗: {str(e)}",
            "data": {}
        }