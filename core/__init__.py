"""Sudharma Music Player, Music for the soul !!"""
# __init__.py

from .song import Song
from .admins import is_sudo, is_admin
from .stream import app, ytdl, safone, pytgcalls, start_stream
from .groups import (
    get_group, get_queue, set_group, set_title, all_groups, clear_queue,
    set_default, shuffle_queue
)
from .funcs import (
    search, check_yt_url, extract_args, generate_cover, delete_messages,
    get_spotify_playlist, get_youtube_playlist
)
from .decorators import language, register, only_admins, handle_error

