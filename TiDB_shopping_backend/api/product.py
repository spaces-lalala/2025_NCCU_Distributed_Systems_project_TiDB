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
    products = (
        db.query(Product)
        .order_by(Product.sold.desc())
        .limit(limit)
        .all()
    )
    return products

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