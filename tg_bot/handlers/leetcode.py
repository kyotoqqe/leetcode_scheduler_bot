from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from ..states import LeetcodeBotMenuState, AddProblemForRepeatState, ViewProblemsState
from ..filters.link_filter import LeetcodeLinkFilter
from ..keyboards.default.menu import bot_menu
from ..keyboards.inline.pagination import pagination_keyboard
from ..keyboards.inline.callback_factory import PageCallback, PrevOrNextCallback
from ..utils.paginator import Paginator
from ..utils.format_data import format_tasks

from infrastructure.utils.schedule import set_scheduler_jobs
from infrastructure.db.query import TaskQuery
from infrastructure.utils.leetcode_api import LeetCodeAPI

leetcode_router = Router()


@leetcode_router.message(Command("info"))
async def more_info(message: types.Message):
    await message.answer("""Для того чтобы взаимодействовать с ботом, 
ты должен должен отправить ссылку на leetcode задачу в формате https://leetcode.com/problems/problem_name/description/,
и тогда это создать напоминание на 1->3->14->30 дней, а после уберет задачу из списка для напоминания.
Когда наступит день повторить задачу, бот отправит напоминание с информацией о ней, а так же ссылкой для ее решения.
Удачи!""")


@leetcode_router.message(Command("leetcode"))
async def leetcode_bot_menu(message: types.Message, state: FSMContext):
    await message.answer("Выбери интересующую опцию из меню:", reply_markup=bot_menu)
    await state.set_state(LeetcodeBotMenuState)


@leetcode_router.message(LeetcodeBotMenuState, F.text.startswith("Добавить"))
async def get_leetcode_problem_link(message: types.Message, state: FSMContext):
    await message.answer("Пришли ссылку на задачу", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AddProblemForRepeatState)


@leetcode_router.message(AddProblemForRepeatState, LeetcodeLinkFilter())
async def add_leetcode_problem(message: types.Message, state: FSMContext, db: TaskQuery, api: LeetCodeAPI, scheduler: AsyncIOScheduler):
    # xсделать пайдантик валидацию
    task_id = await db.create(api, message.text, message.from_user.id)
    set_scheduler_jobs(scheduler, message.bot, db, task_id)
    await message.answer("Задача успешно добавлена.")
    await leetcode_bot_menu(message, state)


@leetcode_router.message(LeetcodeBotMenuState, F.text.startswith("Просмотреть"))
async def leetcode_problems_list(message: types.Message, state: FSMContext, db: TaskQuery):
    await message.answer("Загружаем список задач...", reply_markup=types.ReplyKeyboardRemove())
    tasks = await db.get_list(message.from_user.id)
    tasks = tasks.scalars().all()
    paginator = Paginator(tasks, 2)
    start_from = (paginator.page_size * 0)+1
    text = format_tasks(paginator.page(1), start_from)
    await message.answer(f"""Список добавленных задач:\n{text}""", reply_markup=pagination_keyboard(paginator.get_pages_markup(1)), disable_web_page_preview=True)
    await state.update_data(paginator=paginator, current_page=1)
    await state.set_state(ViewProblemsState)


@leetcode_router.callback_query(PageCallback.filter(F.page_id), ViewProblemsState)
async def get_page_by_id_callback(call: types.CallbackQuery, callback_data: PageCallback, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    paginator = data["paginator"]
    await state.update_data(current_page=callback_data.page_id)
    task_page = paginator.page(callback_data.page_id)
    start_from = paginator.page_size * (callback_data.page_id-1)+1
    text = format_tasks(task_page, start_from)
    await call.message.edit_text(text=text, reply_markup=pagination_keyboard(paginator.get_pages_markup(callback_data.page_id)), disable_web_page_preview=True)


@leetcode_router.callback_query(PrevOrNextCallback.filter(F.direction == "prev"), ViewProblemsState)
async def get_prev_page_callback(call: types.CallbackQuery, callback_data: PrevOrNextCallback, state: FSMContext):
    data = await state.get_data()
    current = data["current_page"]
    paginator = data["paginator"]

    new_page = current - 1

    if new_page < 1:
        await call.answer(
            "В это направлении больше нет доступных страниц.", show_alert=True)
        return

    await state.update_data(current_page=new_page)

    task_page = paginator.page(new_page)
    start_from = paginator.page_size * (new_page-1)+1
    text = format_tasks(task_page, start_from)
    await call.message.edit_text(text=text, reply_markup=pagination_keyboard(paginator.get_pages_markup(new_page)), disable_web_page_preview=True)


@leetcode_router.callback_query(PrevOrNextCallback.filter(F.direction == "next"), ViewProblemsState)
async def get_next_page_callback(call: types.CallbackQuery, callback_data: PrevOrNextCallback, state: FSMContext):
    data = await state.get_data()
    current = data["current_page"]
    paginator = data["paginator"]

    new_page = current + 1

    if new_page > paginator.page_counter:
        await call.answer(
            "В это направлении больше нет доступных страниц.", show_alert=True)
        return

    await state.update_data(current_page=new_page)

    task_page = paginator.page(new_page)
    start_from = paginator.page_size * (new_page-1)+1
    text = format_tasks(task_page, start_from)
    await call.message.edit_text(text=text, reply_markup=pagination_keyboard(paginator.get_pages_markup(new_page)), disable_web_page_preview=True)


@leetcode_router.callback_query(F.data == "menu")
async def cancel_view(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await state.clear()
    await leetcode_bot_menu(call.message, state)


@leetcode_router.message(CommandStart)
async def cmd_start(message: types.Message):
    bot_user = await message.bot.me()
    print(bot_user.username)
    await message.answer(f"""Привет, это {bot_user.username}! 
Это бот который напоминаний который поможет тебе закреплять важные для тебя leetcode задачи.
Используй команды: 
/info - для того чтобы получить больше информации о боте
/leetcode для того чтобы начать пользоваться им""")
