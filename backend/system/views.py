from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache

def health_check(request):
    status = {"postgres": False, "redis": False}

    # Postgres接続確認
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
            status["postgres"] = True
    except Exception as e:
        status["postgres"] = str(e)

    # Redis接続確認
    try:
        cache.set("health_check", "ok", timeout=5)
        if cache.get("health_check") == "ok":
            status["redis"] = True
    except Exception as e:
        status["redis"] = str(e)

    return JsonResponse(status)
