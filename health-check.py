import redis
from fastapi import FastAPI,HTTPException
app=FastAPI()
red = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)
@app.get("/health")
def redis_health():
    try:
        red.ping()
        return {
            "status": "healthy",
            "service": "Redis"
        }
    except redis.RedisError:
        raise HTTPException(
            status_code=503,
            detail="Redis is unavailable"
        )