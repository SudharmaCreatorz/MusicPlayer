"""Sudharma Music Player, Music for the soul !!"""
#song.py

import json
import logging
import asyncio
from shlex import quote
from subprocess import PIPE
from datetime import timedelta
from aiohttp import ClientSession
from pyrogram.types import User, Message
from typing import Dict, Tuple, Union, Optional


class Song:
    """
    Represents a song to be played by the bot

    Attributes:
        title (str): The title of the song
        duration (str): The duration of the song in a human-readable format
        thumb (str): The url of the thumbnail of the song
        remote (str): The url of the song
        source (str): The source of the song (url or file_id)
        headers (dict): The headers to be used when downloading the song
        request_msg (Message): The message that requested the song
        requested_by (User): The user who requested the song
        parsed (bool): Whether the song has been parsed or not
        _retries (int): The number of times the song has been retried
    """

    def __init__(self, link: Union[str, dict], request_msg: Message) -> None:
        """
        Initializes a new Song object

        Args:
            link (str or dict): The url or file_id of the song, or a dictionary
                containing the song's metadata
            request_msg (Message): The message that requested the song
        """
        if isinstance(link, str):
            self.title: str = None
            self.duration: str = None
            self.thumb: str = None
            self.remote: str = None
            self.source: str = link
            self.headers: dict = None
            self.request_msg: Message = request_msg
            self.requested_by: User = request_msg.from_user
            self.parsed: bool = False
            self._retries: int = 0
        elif isinstance(link, dict):
            self.parsed: bool = True
            self._retries: int = 0
            self.duration: str = "N/A"
            self.headers: dict = None
            self.thumb: str = "https://telegra.ph/file/820cac7cb7b1a025542e2.jpg"
            for key, value in link.items():
                setattr(self, key, value)
            self.request_msg: Message = request_msg
            self.requested_by: User = request_msg.from_user

    async def parse(self) -> Tuple[bool, str]:
        """
        Parses the song and retrieves its metadata

        Returns:
            Tuple[bool, str]: A tuple containing a boolean indicating whether the
                parsing was successful and a string with the reason for the failure
        """
        if self.parsed:
            return (True, "ALREADY_PARSED")
        if self._retries >= 5:
            return (False, "MAX_RETRY_LIMIT_REACHED")
        process = await asyncio.create_subprocess_shell(
            f"yt-dlp --print-json --skip-download -f best {quote(self.source)}",
            stdout=PIPE,
            stderr=PIPE,
        )
        out, _ = await process.communicate()
        try:
            video = json.loads(out.decode())
        except json.JSONDecodeError:
            logging.warning("Failed to parse song, retrying")
            self._retries += 1
            return await self.parse()
        check_remote = await self.check_remote_url(video["url"], video["http_headers"])
        check_thumb = await self.check_remote_url(
            video["thumbnail"], video["http_headers"]
        )
        if check_remote and check_thumb:
            self.title = self._escape(video["title"])
            self.duration = str(timedelta(seconds=video["duration"]))
            self.thumb = video["thumbnail"]
            self.remote = video["url"]
            self.headers = video["http_headers"]
            self.parsed = True
            return (True, "PARSED")
        else:
            logging.warning("Failed to parse song, retrying")
            self._retries += 1
            return await self.parse()

    @staticmethod
    async def check_remote_url(
        path: str, headers: Optional[Dict[str, str]] = None
    ) -> bool:
        """
        Checks if a remote url is valid and returns a boolean indicating whether
        the url is valid or not

        Args:
            path (str): The url to check
            headers (dict): The headers to use when checking the url

        Returns:
            bool: Whether the url is valid or not
        """
        try:
            session = ClientSession()
            response = await session.get(path, timeout=5, headers=headers)
            response.close()
            await session.close()
            if response.status == 200:
                return True
            else:
                return False
        except BaseException:
            return False

    @staticmethod
    def _escape(_title: str) -> str:
        """
        Escapes a string to prevent it from being interpreted as markdown

        Args:
            _title (str): The string to escape

        Returns:
            str: The escaped string
        """
        title = _title
        f = ["**", "__", "`", "~~", "--"]
        for i in f:
            title = title.replace(i, f"\\{i}")
        return title

    def to_dict(self) -> Dict[str, str]:
        """
        Converts the song to a dictionary

        Returns:
            Dict[str, str]: A dictionary containing the song's metadata
        """
        return {"title": self.title, "source": self.source}

