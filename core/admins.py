"""Sudharma Music Player, Music for the soul !!"""
#admins.py

import pyrogram
from config import config
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import Message


async def is_sudo(message: Message) -> bool:
    """Check if the message sender is in sudoers list

    Args:
        message (Message): Message to check

    Returns:
        bool: True if the message sender is in sudoers list, else False
    """
    if message is None or message.from_user is None:
        return False

    return message.from_user.id in config.SUDOERS


async def is_admin(message: Message) -> bool:
    """
    Check if the message sender is admin

    Args:
        message (Message): Message to check

    Returns:
        bool: True if the message sender is admin, else False
    """
    if not message or not message.chat:
        return False

    try:
        if message.from_user:
            user: pyrogram.types.ChatMember = await message.chat.get_member(
                message.from_user.id
            )
            if user.status in {
                pyrogram.enums.ChatMemberStatus.OWNER,
                pyrogram.enums.ChatMemberStatus.ADMINISTRATOR,
            }:
                return True
            if message.from_user.id in config.SUDOERS:
                return True
        elif (
            message.sender_chat
            and message.sender_chat.id == message.chat.id
        ):
            return True
    except Exception:
        return False
    return False

