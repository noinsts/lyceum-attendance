from typing import Callable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from src.db.db import session_maker
from src.db.connector import DBConnector


class AdminMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable,
            event: Message | CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        try:
            async with session_maker() as session:
                db = DBConnector(session)
                ids = await db.admins.get_all_ids()
                for id in ids:
                    if id == event.from_user.id:
                        return await handler(event, data)
            return await self._send_denied_message(event)
        except Exception as e:
            raise e
        
    async def _send_denied_message(event: Message | CallbackQuery) -> None:
        prompt = "Немає доступу"
        if isinstance(event, Message):
            await event.answer(prompt)
        elif isinstance(event, CallbackQuery):
            await event.answer(prompt, show_alert=True)
