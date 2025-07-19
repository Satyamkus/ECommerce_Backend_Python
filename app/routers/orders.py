from fastapi import APIRouter
from app.models import OrderRequest
from app.database import order_collection, product_collection
from bson import ObjectId

router = APIRouter()

@router.post("/orders", status_code=201)
async def create_order(order: OrderRequest):
    order_dict = {
        "user_id": order.user_id,
        "items": [item.dict() for item in order.items],
        "total_amount": order.total_amount
    }
    result = await order_collection.insert_one(order_dict)
    return {
        
        "id": str(result.inserted_id)
    }


@router.get("/orders/{user_id}")
async def get_orders(user_id: str, limit: int = 10, offset: int = 0):
    orders_cursor = order_collection.find({"user_id": user_id}).skip(offset).limit(limit)
    orders = []

    async for order in orders_cursor:
        enriched_items = []

        for item in order.get("items", []):
            product_id = item.get("product_id")
            qty = item.get("qty", 1)

            try:
                obj_id = ObjectId(product_id)
                product = await product_collection.find_one({"_id": obj_id})
            except Exception as e:
                product = None

            if product:
                enriched_items.append({
                    "productDetails": {
                        "name": product.get("name", "Unknown"),
                        "id": str(product["_id"])
                    },
                    "qty": qty
                })

        orders.append({
            "id": str(order["_id"]),
            "items": enriched_items,
            "total": order["total_amount"]
        })

    pagination = {
        "next": str(offset + limit),
        "limit": limit,
        "previous": max(offset - limit, 0)
    }

    return {
        "data": orders,
        "page": pagination
    }
