from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.db.query import TaskQuery
from infrastructure.utils.leetcode_api import LeetCodeAPI


class DBConnectionMiddleware(BaseMiddleware):
    def __init__(self, session: AsyncSession, api: LeetCodeAPI):
        self.session = session
        self.api = api

    async def __call__(self, handler, event: Message, data: dict):
        async with self.session() as session:
            data["db"] = TaskQuery(session)
            data["api"] = self.api
            result = await handler(event, data)
        return result
