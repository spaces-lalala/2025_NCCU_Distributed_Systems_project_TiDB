# routes/products.py
from fastapi import APIRouter, HTTPException, Query, Path
from typing import List, Optional
from pydantic import BaseModel
from products import mock_products, mock_categories

router = APIRouter()

# --- Pydantic Models 專屬 products ---

class CategoryOut(BaseModel):
    id: int
    name: str

class ProductOut(BaseModel):
    id: int
    name: str
    price: float
    image_url: Optional[str] = None
    sold: Optional[int]

class ProductDetailOut(ProductOut):
    category: Optional[CategoryOut] = None

class ErrorDetail(BaseModel):
    detail: str

# --- Products API ---

@router.get("/api/products", response_model=List[ProductOut])
def get_products(
    skip: int = 0,
    limit: int = 10,
    category: Optional[str] = None,
    sort_by: Optional[str] = None
):
    products = mock_products.copy()

    # 篩選分類
    if category:
        products = [p for p in products if p["category"] == category]

    # 排序
    if sort_by == "price_asc":
        products.sort(key=lambda x: x["price"])
    elif sort_by == "price_desc":
        products.sort(key=lambda x: -x["price"])
    elif sort_by == "name_asc":
        products.sort(key=lambda x: x["name"])
    elif sort_by == "sold_desc":
        products.sort(key=lambda x: -x["sold"])

    return products[skip: skip + limit]

@router.get("/api/products/bestsellers", response_model=List[ProductOut])
def get_bestsellers(limit: int = 5):
    top_products = sorted(mock_products, key=lambda x: -x["sold"])
    return top_products

@router.get("/api/products/{product_id}", response_model=ProductDetailOut, responses={404: {"model": ErrorDetail}})
def get_product_detail(product_id: int = Path(..., ge=1)):
    product = next((p for p in mock_products if p["id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    category = next((c for c in mock_categories if c["id"] == product["category_id"]), None)
    product_detail = {
        **product,
        "category": category
    }
    return product_detail
