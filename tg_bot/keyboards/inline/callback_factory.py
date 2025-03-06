from aiogram.filters.callback_data import CallbackData


class PageCallback(CallbackData, prefix="paginator"):
    page_id: int


class PrevOrNextCallback(CallbackData, prefix="paginator"):
    direction: str
