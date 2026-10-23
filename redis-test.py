import redis
r = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)
print("Redis Connected:",r.ping())

r.set("student:101", "Madhu", ex=60)
print("TTL to expire:",r.ttl("student:101"))
print("Student:",r.get("student:101"))

r.incr("Page_view")
print("page views:",r.get("page_views"))


r.delete("student:101")
print("After deleting:",r.get("student:101"))