"""Sudharma Music Player, Music for the soul !!"""
#config.py

import os
from dotenv import load_dotenv


load_dotenv()


class Config:
    def __init__(self) -> None:
        """Initialize the Config class."""
        self.API_ID: str | None = os.environ.get("API_ID")
        """Telegram app id, get it from https://my.telegram.org/apps"""
        self.API_HASH: str | None = os.environ.get("API_HASH")
        """Telegram app hash, get it from https://my.telegram.org/apps"""
        self.SESSION: str | None = os.environ.get("SESSION")
        """Pyrogram session string"""
        self.BOT_TOKEN: str | None = os.environ.get("BOT_TOKEN")
        """Your telegram bot token, get it from https://t.me/botfather"""
        self.SUDOERS: list[int] = [
            int(id)
            for id in os.environ.get("SUDOERS", "").split()
            if id.isdigit()
        ]

        if not self.SESSION:
            raise ValueError("SESSION is required! Please check your .env file and try again.")
        if not self.API_ID:
            raise ValueError("API_ID is required! Please check your .env file and try again.")
        if not self.API_HASH:
            raise ValueError("API_HASH is required! Please check your .env file and try again.")
        self.SPOTIFY: bool = False
        """Spotify client id and secret, get it from https://developer.spotify.com/dashboard/applications"""
        self.QUALITY: str = os.environ.get("QUALITY", "high").lower()
        """An available stream quality (read the README.md for more info)"""
        self.PREFIXES: list[str] = os.environ.get("PREFIX", "!").split()
        """An available bot language (read the README.md for more info)"""
        self.LANGUAGE: str = os.environ.get("LANGUAGE", "en").lower()
        """An available stream mode like audio or video (read the README.md for more info)"""
        self.STREAM_MODE: str = (
            "audio"
            if (os.environ.get("STREAM_MODE", "audio").lower() == "audio")
            else "video"
        )
        self.ADMINS_ONLY: bool = os.environ.get("ADMINS_ONLY", "False").lower() == "true"
        """Change it to 'True' if you want to make /play commands only for admins"""
        self.SPOTIFY_CLIENT_ID: str | None = os.environ.get("SPOTIFY_CLIENT_ID")
        self.SPOTIFY_CLIENT_SECRET: str | None = os.environ.get("SPOTIFY_CLIENT_SECRET")
print("Config loaded successfully!")

config = Config()
