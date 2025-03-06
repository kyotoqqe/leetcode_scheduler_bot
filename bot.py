from aiogram import Bot, Dispatcher
import asyncio
import aiohttp
import betterlogging as bl
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.redis import RedisJobStore


from tg_bot.config import load_config
from tg_bot.handlers.leetcode import leetcode_router
from tg_bot.handlers.errors import error_router
from infrastructure.db.connection import create_engine, create_session
from infrastructure.utils.leetcode_api import LeetCodeAPI
from tg_bot.middlewares.session_middleware import DBConnectionMiddleware
from tg_bot.middlewares.scheduler_middleware import SchedulerMiddleware
import os


async def main():
    bl.basic_colorized_config(level=logging.INFO)
    config = load_config(os.path.join(os.path.dirname(__file__), ".env"))
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()
    job_stores = {
        "default": RedisJobStore(
            jobs_key="dispatched_trips_jobs", run_times_key="dispatched_trips_running", host=config.redis.host, port=config.redis.port
        )
    }
    scheduler = AsyncIOScheduler(job_stores)
    db = create_engine(config.db)
    async with aiohttp.ClientSession() as session:
        leetcode_api = LeetCodeAPI(session)
        leetcode_router.message.middleware(
            DBConnectionMiddleware(session=create_session(db), api=leetcode_api))
        leetcode_router.message.middleware(
            SchedulerMiddleware(scheduler=scheduler))
        dp.include_routers(leetcode_router, error_router)
        scheduler.start()
        await dp.start_polling(bot)
        await bot.session.close()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    logging.info("Bot stopped!")
