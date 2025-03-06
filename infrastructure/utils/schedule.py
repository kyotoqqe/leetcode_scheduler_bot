from aiogram import Bot
from apscheduler.jobstores.base import ConflictingIdError
import logging

from ..db.query import TaskQuery
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class TaskSchedulerError(Exception):
    """Ошибка создания задачи"""


async def leetcode_task_notification(bot: Bot, db: TaskQuery, task_id: int, last: bool = False):
    task = await db.get_single(task_id)
    await bot.send_message(chat_id=task.user_id, text=f"""Привет! Пришло время повторить эту задачу:
Название: {task.title}
Сложность: {task.difficulty.value}
Ссылка на задачу: {task.link}""", disable_web_page_preview=True)

    if last:
        await db.delete(task_id)


def set_scheduler_jobs(scheduler, bot, db, task_id):
    days = [1, 3, 14, 30]
    try:
        for i in days:
            run_time = datetime.now()+timedelta(days=i)
            scheduler.add_job(leetcode_task_notification,
                              "date", run_date=run_time, args=(bot, db, task_id, i == days[-1]))
    except ConflictingIdError:
        logger.warning(f"Задача {task_id} уже существует в расписании!")
    except Exception as e:
        db.delete(task_id)
        logger.error(f"Ошибка создания задач для task_id={task_id}: {e}")
        raise TaskSchedulerError(f"Произошла ошибка создания задач {e}")
