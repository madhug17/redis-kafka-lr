import redis
from fastapi import FastAPI, HTTPException
app=FastAPI()
red = redis.Redis(
    host="localhost",
    decode_responses=True,
    port=6379
)
@app.get("/limited")
def limited_endpoint():
    user_id = "user101"
    key = f"rate_limit:{user_id}"
    count = red.incr(key)
    if count==1:
        red.expire(key,60)
    if count >= 5:
        raise HTTPException(
            status_code=404,
            detail="Too many request so wait for 1 minute"
        )
    return {
        "message" : "Request allowed",
        "requests_used": count,
        "limit": 5,
        "ttl":red.ttl(key)
    }