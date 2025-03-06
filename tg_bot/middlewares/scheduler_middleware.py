from aiogram.dispatcher.middlewares.base import BaseMiddleware


class SchedulerMiddleware(BaseMiddleware):
    def __init__(self, scheduler):
        super().__init__()
        self.scheduler = scheduler

    async def __call__(self, handler, event, data):
        data["scheduler"] = self.scheduler
        return await handler(event, data)
