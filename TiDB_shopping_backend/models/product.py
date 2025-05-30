# 重新匯出 Product 類別，避免重複定義
from .order import Product, Category

__all__ = ['Product', 'Category']