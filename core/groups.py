"""Sudharma Music Player, Music for the soul !!"""
#groups.py

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, Union

from pyrogram import Client
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.phone import EditGroupCallTitle
from pyrogram.types import Message

from config import config
from core import Song
from core.queue import Queue

_LOGGER = logging.getLogger(__name__)

GROUPS: Dict[int, Dict[str, Any]] = {}


def all_groups() -> List[int]:
    """Return a list of all groups."""
    try:
        if not GROUPS:
            raise ValueError("GROUPS is empty!")
        return list(GROUPS.keys())
    except Exception as e:
        _LOGGER.error(f"An error occurred: {e}")
        raise


def set_default(chat_id: int) -> None:
    """Set default values for a group."""
    global GROUPS  # pylint: disable=global-statement
    try:
        if chat_id is None:
            raise ValueError("Chat ID cannot be None")
        
        GROUPS[chat_id] = {
            "is_playing": False,
            "now_playing": None,
            "stream_mode": config.STREAM_MODE,
            "admins_only": config.ADMINS_ONLY,
            "loop": False,
            "lang": config.LANGUAGE,
            "queue": Queue(),
        }
    except Exception as e:
        _LOGGER.error(f"Failed to set default values for chat ID {chat_id}: {e}")
        raise


def get_group(chat_id: int) -> Dict[str, Any]:
    """Get a group by chat_id."""
    try:
        if chat_id is None:
            raise ValueError("Chat ID cannot be None")
        if chat_id not in GROUPS:
            set_default(chat_id)
        return GROUPS[chat_id]
    except Exception as e:
        _LOGGER.error(f"An error occurred while getting group for chat ID {chat_id}: {e}")
        raise


def set_group(chat_id: int, **kwargs: Any) -> None:
    """Set a value for a group."""
    global GROUPS
    try:
        if chat_id is None:
            raise ValueError("Chat ID cannot be None")
        if chat_id not in GROUPS:
            raise KeyError(f"Chat ID {chat_id} does not exist in GROUPS")
        for key, value in kwargs.items():
            if key not in GROUPS[chat_id]:
                raise KeyError(f"Key '{key}' is not a valid group attribute")
            GROUPS[chat_id][key] = value
    except Exception as e:
        _LOGGER.error(f"Failed to set group values for chat ID {chat_id}: {e}")
        raise


async def set_title(
    client: Client, message_or_chat_id: Union[Message, int], title: str
) -> None:
    """Set the title of a group."""
    chat_id: int
    if isinstance(message_or_chat_id, Message):
        chat_id = message_or_chat_id.chat.id
    elif isinstance(message_or_chat_id, int):
        chat_id = message_or_chat_id
    else:
        raise TypeError("Message or chat_id must be an instance of Message or int")
    try:
        # Check if the chat exists
        peer = await client.resolve_peer(chat_id)
        if peer is None:
            raise ValueError(f"Chat ID {chat_id} does not exist")
        # Check if the chat has a title
        chat = await client.invoke(GetFullChannel(channel=peer))
        if chat is None or chat.full_chat.call is None:
            raise ValueError(f"Chat ID {chat_id} does not have a title")
        # Set the title
        await client.invoke(EditGroupCallTitle(call=chat.full_chat.call, title=title))
    except AttributeError as e:
        # Handle null pointer references
        _LOGGER.exception("Error setting title: %s", e)
        raise AttributeError("Null pointer reference encountered") from e
    except BaseException as e:
        # Handle unhandled exceptions
        _LOGGER.exception("Error setting title: %s", e)
        raise


def get_queue(chat_id: int) -> Queue[Song]:
    """Get the queue of a group."""
    global GROUPS
    try:
        if chat_id is None:
            raise ValueError("Chat ID cannot be None")
        if chat_id not in GROUPS:
            raise KeyError(f"Chat ID {chat_id} does not exist in GROUPS")
        return GROUPS[chat_id]["queue"]
    except AttributeError as e:
        # Handle null pointer references
        _LOGGER.exception("Error getting queue: %s", e)
        raise AttributeError("Null pointer reference encountered") from e
    except BaseException as e:
        # Handle unhandled exceptions
        _LOGGER.exception("Error getting queue: %s", e)
        raise


def clear_queue(chat_id: int) -> None:
    """Clear the queue of a group."""
    global GROUPS  # pylint: disable=global-statement
    try:
        if chat_id is None:
            raise ValueError("Chat ID cannot be None")
        if chat_id not in GROUPS:
            raise KeyError(f"Chat ID {chat_id} does not exist in GROUPS")
        if GROUPS[chat_id]["queue"] is None:
            raise AttributeError("Null pointer reference encountered")
        GROUPS[chat_id]["queue"].clear()
    except AttributeError as e:
        # Handle null pointer references
        _LOGGER.exception("Error clearing queue: %s", e)
        raise AttributeError("Null pointer reference encountered") from e
    except BaseException as e:
        # Handle unhandled exceptions
        _LOGGER.exception("Error clearing queue: %s", e)
        raise


def shuffle_queue(chat_id: int) -> Queue[Song]:
    """Shuffle the queue of a group."""
    global GROUPS
    try:
        if chat_id is None:
            raise ValueError("Chat ID cannot be None")
        if chat_id not in GROUPS:
            raise KeyError(f"Chat ID {chat_id} does not exist in GROUPS")
        queue = GROUPS[chat_id]["queue"]
        if queue is None:
            raise AttributeError("Null pointer reference encountered")
        queue.shuffle()
        return queue
    except AttributeError as e:
        # Handle null pointer references
        _LOGGER.exception("Error shuffling queue: %s", e)
        raise AttributeError("Null pointer reference encountered") from e
    except BaseException as e:
        # Handle unhandled exceptions
        _LOGGER.exception("Error shuffling queue: %s", e)
        raise

