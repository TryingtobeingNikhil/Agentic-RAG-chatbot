"""
Chat history storage — MongoDB-backed with automatic in-memory fallback.

If MongoDB is unavailable (no URL set, or connection fails), the module
automatically falls back to the in-memory implementation and logs:
  "MongoDB unavailable, using in-memory chat history"
"""

import logging
from typing import List

from langchain_core.messages import BaseMessage

from src.db.mongo_client import db

logger = logging.getLogger(__name__)

# Determine at import time whether MongoDB is available
_mongo_available = db is not None

if not _mongo_available:
    logger.warning("MongoDB unavailable, using in-memory chat history")
    from src.memory.chathistory_in_memory import ChatInMemoryHistory as _InMemory


# ---------------------------------------------------------------------------
# MongoDB implementation (used only when db is available)
# ---------------------------------------------------------------------------

class MongoDBChatMessageHistory:
    """Chat history backed by MongoDB."""

    def __init__(self, session_id: str):
        """
        Initialize chat history for a session.

        Args:
            session_id: Unique session identifier.
        """
        self.session_id = session_id
        self._collection = db["chat_history"]

    async def add_message(self, message: BaseMessage) -> None:
        """
        Save a message to MongoDB.

        Args:
            message: The message to save.
        """
        from datetime import datetime
        await self._collection.insert_one({
            "session_id": self.session_id,
            "type": message.type,
            "content": message.content,
            "additional_kwargs": message.additional_kwargs,
            "timestamp": datetime.utcnow(),
        })

    async def get_messages(self) -> List[BaseMessage]:
        """
        Load all messages for a session from MongoDB.

        Returns:
            List of messages in chronological order.
        """
        from langchain_core.messages import messages_from_dict

        cursor = self._collection.find(
            {"session_id": self.session_id}
        ).sort("timestamp", 1)
        docs = await cursor.to_list(length=1000)

        return messages_from_dict([
            {
                "type": d["type"],
                "data": {
                    "content": d["content"],
                    "additional_kwargs": d.get("additional_kwargs", {}),
                },
            }
            for d in docs
        ])

    async def clear(self) -> None:
        """Delete all messages for a session."""
        await self._collection.delete_many({"session_id": self.session_id})


# ---------------------------------------------------------------------------
# In-memory shim — wraps ChatInMemoryHistory so it is async-compatible
# ---------------------------------------------------------------------------

class _InMemoryAsyncHistory:
    """Async-compatible wrapper around the synchronous in-memory store."""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self._history = _InMemory.get_session_history(session_id)

    async def add_message(self, message: BaseMessage) -> None:
        self._history.add_message(message)

    async def get_messages(self) -> List[BaseMessage]:
        return self._history.messages

    async def clear(self) -> None:
        _InMemory.clear_history(self.session_id)


# ---------------------------------------------------------------------------
# Public factory — picks the right backend transparently
# ---------------------------------------------------------------------------

class ChatHistory:
    """Factory that returns MongoDB or in-memory chat history transparently."""

    @classmethod
    def get_session_history(cls, session_id: str, config: dict = None):
        """
        Get or create chat history for a session.

        Args:
            session_id: Unique session identifier.
            config: Optional configuration dictionary (unused, kept for API compat).

        Returns:
            An async-compatible chat history instance.
        """
        if _mongo_available:
            return MongoDBChatMessageHistory(session_id)
        return _InMemoryAsyncHistory(session_id)
