import asyncio

from app import main


def extract(context):
    asyncio.get_event_loop().run_until_complete(main.run())
