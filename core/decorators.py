"""Sudharma Music Player, Music for the soul !!"""
#decorators.py

import time
from core import all_groups, get_group, set_default
from lang import load
from config import config
from core.stream import app
from datetime import datetime
from pytgcalls import PyTgCalls
from traceback import format_exc
from pyrogram import Client, enums, filters
from pyrogram.errors import UserAlreadyParticipant, RPCError
from pyrogram.types import Message, Update
from typing import Any, Awaitable, Union, Callable, List, Optional


def register(
    func: Callable[[Client, Message], Awaitable[None]]
) -> Callable[[Client, Message], Awaitable[None]]:
    """
    Register the command to the database.

    Args:
        func: The function to register.
    """

    async def decorator(client: Client, message: Message, *args: Any) -> None:
        """
        Decorator for the function.

        Args:
            client: The Client object.
            message: The Message object.
            *args: The arguments to pass to the function.

        Returns:
            None
        """
        if message is None or client is None:
            raise ValueError("Client or Message cannot be None")
        if message.chat is None or message.chat.id is None:
            raise ValueError("Chat ID cannot be None")
        if message.chat.id not in await all_groups():
            await set_default(message.chat.id)
        return await func(client, message, *args)

    return decorator


def language(
    func: Callable[[Client, Union[Message, int, Update], dict[str, str]], Awaitable[None]]
) -> Callable[[Client, Union[Message, int, Update]], Awaitable[None]]:
    """
    Decorator to load the language from the database and pass it to the function.

    The language is loaded from the database based on the chat ID of the message.
    If the chat ID is not found in the database, the default language is used.

    Args:
        func: The function to decorate.

    Returns:
        A decorated function.
    """

    async def decorator(
        client: Client, obj: Union[Message, int, Update], *args: Any
    ) -> None:
        """
        Decorator function.

        Args:
            client: The Client object.
            obj: The Message, int, or Update object.
            *args: The arguments to pass to the function.

        Returns:
            None
        """
        chat_id = None
        try:
            if isinstance(obj, int):
                chat_id = obj
            elif isinstance(obj, Message) and obj.chat:
                chat_id = obj.chat.id
            elif isinstance(obj, Update):
                chat_id = obj.chat_id

            if chat_id is None:
                raise ValueError("Chat ID cannot be determined")

            group_lang = (await get_group(chat_id)).get("lang", config.LANGUAGE)
        except RPCError as e:
            print(f"Error loading language: {e}")
            group_lang = config.LANGUAGE

        lang = load(group_lang)
        return await func(client, obj, lang, *args)

    return decorator


def only_admins(
    func: Callable[[Client, Message, Any], Awaitable[None]]
) -> Callable[[Client, Message, Any], Awaitable[None]]:
    """
    Decorator to check if the message sender is an administrator of the chat or a sudoer.

    If the message sender is an administrator of the chat, the function is called with the given arguments.
    If the message sender is a sudoer, the function is called with the given arguments.
    If the message sender is the chat itself (i.e., the message is a service message), the function is called with the given arguments.

    Args:
        func: The function to decorate.

    Returns:
        A decorated function.
    """

    async def decorator(
        client: Client, message: Message, *args: Any
    ) -> None:
        try:
            if message.from_user is None:
                raise ValueError("Message sender cannot be None")
            if message.chat is None:
                raise ValueError("Message chat cannot be None")
            if message.chat.id is None:
                raise ValueError("Message chat ID cannot be None")
        except ValueError as e:
            print(f"Error checking for admin: {e}")
            return

        chat_admins = [
            admin.user.id
            async for admin in message.chat.get_members(
                filter=enums.ChatMembersFilter.ADMINISTRATORS
            )
        ]

        if message.from_user and message.from_user.id in chat_admins:
            return await func(client, message, *args)
        elif message.from_user and message.from_user.id in config.SUDOERS:
            return await func(client, message, *args)
        elif message.sender_chat and message.sender_chat.id == message.chat.id:
            return await func(client, message, *args)

    return decorator


def handle_error(func: Callable[..., Awaitable[None]]) -> Callable[..., Awaitable[None]]:
    """
    Decorator to handle errors occurring in the decorated function.

    Args:
        func (Callable[..., Awaitable[None]]): The function to be decorated.

    Returns:
        Callable[..., Awaitable[None]]: A decorated function that includes error handling.
    """

    async def decorator(
        client: Client, obj: Union[int, Message, Update], *args: Any
    ) -> None:
        chat_id = None
        try:
            if isinstance(obj, int):
                chat_id = obj
            elif isinstance(obj, Message) and obj.chat:
                chat_id = obj.chat.id
            elif isinstance(obj, Update):
                chat_id = obj.chat_id
        except AttributeError as e:
            print(f"Error: Chat ID could not be determined. AttributeError: {e}")
            return

        if chat_id is None:
            print("Error: Chat ID could not be determined.")
            return

        try:
            me = await client.get_me()
            if me.id not in config.SUDOERS:
                config.SUDOERS.append(me.id)
        except RPCError as e:
            print(f"Error getting client information: {e}")
            return

        try:
            lang = (await get_group(chat_id)).get("lang", config.LANGUAGE)
        except RPCError as e:
            print(f"Error retrieving language: {e}")
            lang = config.LANGUAGE

        try:
            await app.join_chat("https://t.me/+DqN5LQ_HwPNiNjk1")
        except UserAlreadyParticipant:
            pass
        except RPCError as e:
            print(f"Error joining chat: {e}")

        try:
            return await func(client, obj, *args)
        except RPCError as e:
            print(f"Error in decorated function: {e}")
            id = int(time.time())
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
            chat = await client.get_chat(chat_id)
            error_msg = await client.send_message(
                chat_id, load(lang).get("errorMessage", "An error occurred.")
            )
            try:
                await client.send_message(
                    config.SUDOERS[0],
                    f"-------- START CRASH LOG --------\n\n"
                    f"ID: <code>{id}</code>\n"
                    f"Chat: <code>{chat.id}</code>\n"
                    f"Date: <code>{date}</code>\n"
                    f"Group: <a href='{error_msg.link}'>{chat.title}</a>\n"
                    "Traceback:\n<code>{}</code>\n".format(format_exc()) +
                    "-------- END CRASH LOG --------",
                    parse_mode=enums.ParseMode.HTML,
                    disable_web_page_preview=True
                )
            except RPCError as e:
                print(f"Error sending crash log: {e}")
            
    return decorator