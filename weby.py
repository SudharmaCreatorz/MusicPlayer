"""Sudharma Music Player, Music for the soul !!"""
# weby.py

from pyrogram import Client
from flask import Flask
from config import Config
import os

config = Config()

app = Flask(__name__)

@app.route('/')
def health_check() -> tuple[str, int]:
    """
    A health check endpoint which responds with a 200 OK status code and a message
    indicating that the Music Player is running.

    Returns:
        tuple[str, int]: A tuple containing the response message and the HTTP status code.

    Raises:
        TypeError: If `app` is not an instance of Flask.
        AttributeError: If `config` does not have all the required attributes.
        ValueError: If a configuration value is not valid.
    """
    required_attrs: dict[str, type] = {
        "API_ID": str,
        "API_HASH": str,
        "SESSION": str,
        "BOT_TOKEN": str,
        "SUDOERS": list,
        "QUALITY": str,
        "PREFIXES": list,
        "LANGUAGE": str,
        "STREAM_MODE": str,
        "ADMINS_ONLY": bool,
        "SPOTIFY_CLIENT_ID": str,
        "SPOTIFY_CLIENT_SECRET": str,
    }

    try:
        if not isinstance(app, Flask):
            raise TypeError("app is not an instance of Flask")

        for attr, expected_type in required_attrs.items():
            if not hasattr(config, attr):
                raise AttributeError(f"config has no attribute '{attr}'")

            attr_value = getattr(config, attr, None)

            if attr_value is None:
                raise ValueError(f"{attr} is not set")

            if not isinstance(attr_value, expected_type):
                raise ValueError(f"{attr} is not a valid {expected_type.__name__}")

            if attr == "API_ID" and not str(attr_value).isdigit():
                raise ValueError("API_ID is not a valid Telegram API ID")

        return "Sudharma Music Player is running!", 200

    except (TypeError, AttributeError, ValueError) as error:
        return f"Error: {error}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

