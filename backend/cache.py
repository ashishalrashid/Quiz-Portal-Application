import json
import logging
import os
from typing import Any, Optional

import redis

logger = logging.getLogger(__name__)

redis_client: Optional[redis.Redis] = None


def init_cache(app) -> None:
    """
    Initialize a Redis client. Falls back to no-op if Redis is unavailable.
    """
    global redis_client
    url = app.config.get("REDIS_URL") or os.getenv("REDIS_URL") or "redis://localhost:6379/0"
    try:
        redis_client = redis.Redis.from_url(url)
        redis_client.ping()
        app.logger.info("Redis cache enabled at %s", url)
    except Exception as exc:  # pragma: no cover - best-effort init
        redis_client = None
        app.logger.warning("Redis cache disabled: %s", exc)


def cache_get_json(key: str) -> Optional[Any]:
    if not redis_client:
        return None
    try:
        raw = redis_client.get(key)
        return json.loads(raw) if raw else None
    except Exception:  # pragma: no cover - cache should be best-effort
        return None


def cache_set_json(key: str, value: Any, ex: int = 60) -> None:
    if not redis_client:
        return
    try:
        redis_client.set(key, json.dumps(value), ex=ex)
    except Exception:  # pragma: no cover
        pass


def cache_delete_pattern(pattern: str) -> None:
    if not redis_client:
        return
    try:
        for key in redis_client.scan_iter(match=pattern):
            redis_client.delete(key)
    except Exception:  # pragma: no cover
        pass

