from upstash_redis import Redis
from app.core.config import settings
import json

# Create Redis client (REST-based)
redis_client = Redis(
    url=settings.redis_url,
    token=settings.redis_token
)


def get_session(session_id: str) -> dict:
    """
    Fetch conversation/session data from Redis.
    """
    data = redis_client.get(session_id)
    if not data:
        return {}
    return json.loads(data)


def save_session(session_id: str, data: dict, ttl_seconds: int = 1800):
    """
    Save conversation/session data to Redis with TTL.
    Default TTL = 30 minutes.
    """
    redis_client.set(session_id, json.dumps(data), ex=ttl_seconds)


def clear_session(session_id: str):
    """
    Delete session data from Redis.
    """
    redis_client.delete(session_id)



##############################
# #new changes

from datetime import datetime

# ===== Post-submission correction window =====

CORRECTION_TTL = 300  # 5 minutes


def save_last_ticket(session_id: str, ticket_id: str):
    """
    Store last submitted ticket for correction window.
    """
    key = f"correction:{session_id}"
    value = {
        "ticket_id": ticket_id,
        "submitted_at": datetime.utcnow().isoformat()
    }
    redis_client.set(key, json.dumps(value), ex=CORRECTION_TTL)


def get_last_ticket(session_id: str) -> dict | None:
    """
    Fetch last submitted ticket (if within correction window).
    """
    key = f"correction:{session_id}"
    data = redis_client.get(key)
    return json.loads(data) if data else None

