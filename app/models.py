
#     id: str

# # Orders
# class OrderRequest(BaseModel):
#     user_id: str
#     product_ids: List[str]
#     total_amount: float

# class OrderResponse(OrderRequest):
#     id: str

from pydantic import BaseModel
from typing import List, Optional

# Size Entry for Products

class SizeEntry(BaseModel):
    size: str
    quantity: int


# Product Models

class ProductRequest(BaseModel):
    name: str
    price: float
    sizes: List[SizeEntry]

class ProductResponse(BaseModel):
    id: str
    name: str
    price: float


# Order Models

class OrderItem(BaseModel):
    product_id: str
    qty: int

class OrderRequest(BaseModel):
    user_id: str
    items: List[OrderItem]
    total_amount: float

class ProductDetails(BaseModel):
    name: str
    id: str

class OrderItemResponse(BaseModel):
    productDetails: ProductDetails
    qty: int

class OrderResponse(BaseModel):
    id: str
    items: List[OrderItemResponse]
    total: float


