from django.http import JsonResponse
from django.core.cache import cache
from django.db import connection

def health(request):
    # Redis: set/get
    cache.set("ping", "pong", 10)
    redis_ok = cache.get("ping") == "pong"

    # Postgres: SELECT 1
    try:
        with connection.cursor() as cur:
            cur.execute("SELECT 1;")
        db_ok = True
    except Exception:
        db_ok = False

    return JsonResponse({"status": "ok", "postgres": db_ok, "redis": redis_ok})
