import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from .handlers import get_router
from .middlewares.db import DBMiddleware
from .db.db import create_db, drop_db

load_dotenv()
TOKEN = os.getenv("TOKEN")


class LyceumBot:
    def __init__(self) -> None:
        self.bot = Bot(token=TOKEN)
        self.dp = None
        self.storage = None

    async def run(self) -> None:
        try:
            #await drop_db()
            await create_db()

            self.dp = Dispatcher(storage=self.storage)

            db_middleware = DBMiddleware()
            self.dp.message.middleware(db_middleware)
            self.dp.callback_query.middleware(db_middleware)

            self.dp.include_router(get_router())
            await self.dp.start_polling(self.bot)

        except Exception as e:
            raise e
        finally:
            await self.bot.session.close()
