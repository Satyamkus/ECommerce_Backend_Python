

from fastapi import APIRouter
from typing import Optional
from app.models import ProductRequest, ProductResponse
from app.database import product_collection
from bson import ObjectId
import re

router = APIRouter()

@router.post("/products", status_code=201)
async def create_product(product: ProductRequest):
    result = await product_collection.insert_one(product.dict())
    return {"id": str(result.inserted_id)}

@router.get("/products")
async def list_products(name: Optional[str] = None, size: Optional[str] = None, limit: int = 10, offset: int = 0):
    query = {}
    if name:
        query["name"] = {"$regex": re.compile(name, re.IGNORECASE)}
    if size:
        query["sizes.size"] = size

    cursor = product_collection.find(query).skip(offset).limit(limit)
    results = []
    async for doc in cursor:
        results.append({
            "id": str(doc["_id"]),
            "name": doc["name"],
            "price": doc["price"]
        })

    pagination = {
        "next": str(offset + limit),
        "limit": limit,
        "previous": max(offset-limit , 0)
    }

    return {
        "data": results,
        "page": pagination
    }
