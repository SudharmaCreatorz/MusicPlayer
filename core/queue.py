"""Sudharma Music Player, Music for the soul !!"""
#queue.py

import logging
import random
from asyncio import Queue as AsyncQueue
from typing import Any, Iterator, List, Optional, TypeVar

from pyrogram import Client
from pyrogram.types import Message

from core import Song

_T = TypeVar('_T')

LOGGER = logging.getLogger(__name__)


class Queue(AsyncQueue[_T]):
    """A queue for storing songs to be played."""

    def __init__(self) -> None:
        """Initialize the queue."""
        super().__init__()

    def clear(self) -> None:
        """Clear the queue."""
        LOGGER.debug("Clearing the queue")
        self._queue.clear()
        self._init(0)

    def shuffle(self) -> "Queue[_T]":
        """Shuffle the queue."""
        LOGGER.debug("Shuffling the queue")
        copy = list(self._queue.copy())
        random.shuffle(copy)
        self.clear()
        self._queue.extend(copy)
        return self

    def __iter__(self) -> Iterator[_T]:
        """Return an iterator over the queue."""
        self.__index = 0
        return self

    def __next__(self) -> _T:
        """Get the next item from the queue."""
        if self.__index >= len(self):
            raise StopIteration

        item = self._queue[self.__index]
        self.__index += 1
        return item

    def __len__(self) -> int:
        """Return the length of the queue."""
        return len(self._queue)

    def __getitem__(self, index: int) -> _T:
        """Get an item from the queue by index."""
        return self._queue[index]

    def __str__(self) -> str:
        """Return a string representation of the queue."""
        queue = list(self._queue)
        string = ""
        for x, item in enumerate(queue):
            if x < 10:
                string += f"**{x+1}. [{item.title}]({item.source})** \n- Requested By: {item.requested_by.mention if item.requested_by else item.request_msg.sender_chat.title}\n"
            else:
                string += f"`\n...{len(queue)-10}`"
                return string
        return string


def get_queue(chat_id: int) -> Queue[Song]:
    """Get the queue for a chat."""
    LOGGER.debug("Getting the queue for chat %d", chat_id)
    return Queue()

