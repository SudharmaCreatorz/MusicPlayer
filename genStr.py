"""Sudharma Music Player, Music for the soul !!"""
#genStr.py

"""
Generate a pyrogram session string
"""
from pyrogram import Client


async def main() -> None:
    """Main function to generate a pyrogram session string

    Ask the user for their Telegram API ID and API Hash, create a
    Client instance, and then print the session string returned by
    Client.export_session_string
    """
    try:
        api_id: int = int(input("API ID: "))
        api_hash: str = input("API HASH: ")

        # Check for null pointer references
        if not api_id or not api_hash:
            print("API ID and API Hash are required!")
            return

        app = Client("my_app", api_id=api_id, api_hash=api_hash, in_memory=True)
        async with app:
            session_string: str = await app.export_session_string()
            print(session_string)
    except ValueError as ve:
        print(f"An error occurred: {ve}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())

