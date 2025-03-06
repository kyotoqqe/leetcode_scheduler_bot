from aiogram import types, Router, F
from aiogram.filters.exception import ExceptionTypeFilter
from infrastructure.utils.leetcode_api import LeetcodeAPIError, ParsingError
from infrastructure.utils.schedule import TaskSchedulerError
from ..utils.paginator import PaginatorError

error_router = Router()


@error_router.error(ExceptionTypeFilter(LeetcodeAPIError), F.update.message.as_("message"))
async def handle_leetcode_api_error(err: types.ErrorEvent, message: types.Message):
    await message.reply(f"Ошибка запроса к API {err.exception}")


@error_router.error(ExceptionTypeFilter(ParsingError), F.update.message.as_("message"))
async def handle_parsing_error(err: types.ErrorEvent, message: types.Message):
    await message.reply(f"Неверный формат ссылки! {err.exception}")


@error_router.error(ExceptionTypeFilter(TaskSchedulerError), F.update.message.as_("message"))
async def handle_task_creation_error(err: types.ErrorEvent, message: types.Message):
    await message.reply(f"Задача не была создана! Произошла ошибка {err.exception}")


@error_router.error(ExceptionTypeFilter(PaginatorError), F.update.message.as_("message"))
async def handle_task_creation_error(err: types.ErrorEvent, message: types.Message):
    await message.reply(f"Не удалось получить список задач! Произошла ошибка {err.exception}")
