import asyncio
import os
import nest_asyncio

from async_icq.bot import AsyncBot
from aiologger.levels import LogLevel


nest_asyncio.apply()


notifier = AsyncBot(
    token=os.getenv('TOKEN'),
    url=os.getenv('API_URL'),
    loop=asyncio.get_event_loop(),
    log_level=LogLevel.DEBUG
)
