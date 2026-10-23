import json 
import redis
from fastapi import FastAPI,HTTPException
app = FastAPI()
import time

red = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)
products = {

    101: {"name": "Laptop", "price": 50000},
    102: {"name": "Keyboard", "price": 1500},
    103: {"name": "Mouse", "price": 700}
}

@app.get("/products/{product_id}")
def get_product(product_id:int):
    start=time.time()
    cache_key = f"cache:product:{product_id}"
    cache_products = red.get(cache_key)
    if cache_products is not None:
        return{
            "source": "Redis cache",
            "product": json.loads(cache_products)
        }
    product = products.get(product_id)
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    red.set(cache_key, json.dumps(product), ex=60)
    return{
        "source": "Simulated database",
        "product": product
    }

@app.get("/products/name/{product_name}")
def get_product(product_name:str):
    cache_key = f"Cache:product:{product_name}"
    cached_product=red.get(cache_key)
    if cached_product is not None:
        return {
            "source": "Redis cache",
            "product": json.loads(cached_product)
        }
    product = next(
        (p for p in products.values()
         if p['name'].lower() == product_name.lower()),
         None
    )
    if product is None:
        raise HTTPException(status_code=404,detail="product not found")
    red.set(cache_key,json.dumps(product),ex=60)
    return {
        "source": "Simulated database",
        "product": product
    }

"""
what if the price will changes but still the redis will contains same price so wht to do now

SOLUTION: Step 2: Invalidate the cache
Delete the outdated Redis entry using DEL.
red.delete("cache:product:101")

Step 3: Next request
Redis reports a cache miss, the app fetches the updated product, and Redis stores the new price.
"""

@app.put("/products/{product_id}/price")
def update_price(product_id:int,new_price:float):
    product = products.get(product_id)
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    product["price"] = new_price
    red.delete(f"cache:product:{product_id}")
    return {
        "message": "Product price updated",
        "product": product
    }
@app.put("/test/stale-cache")
def test_scale():
    products[101]['price'] = 45000
    cached_product = red.get("cache:product:101")
    return{
        "database_price": products[101]["price"],
        "redis_cached_product": (
            json.loads(cached_product)
            if cached_product is not None
            else None
        )
    }