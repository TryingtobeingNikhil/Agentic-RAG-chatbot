"""
MongoDB client initialization (optional).

If MONGODB_URL is not set or connection fails, a None db is returned and
the application will automatically fall back to in-memory chat history.
"""

import logging

logger = logging.getLogger(__name__)

db = None

try:
    import os
    from motor.motor_asyncio import AsyncIOMotorClient
    from src.core.config import settings

    _mongo_url = settings.MONGODB_URL
    if not _mongo_url:
        raise ValueError("MONGODB_URL is not set")

    _client = AsyncIOMotorClient(_mongo_url, serverSelectionTimeoutMS=3000)
    db = _client[settings.MONGODB_DB_NAME]
    logger.info("MongoDB client initialized at %s", _mongo_url)

except Exception as exc:
    logger.warning("MongoDB unavailable, using in-memory chat history: %s", exc)
    db = None
