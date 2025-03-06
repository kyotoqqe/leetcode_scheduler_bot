from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .callback_factory import PageCallback, PrevOrNextCallback


def pagination_keyboard(pages):
    inline_keyboard = []
    pages_row = []
    for i, page in enumerate(pages, start=1):
        pages_row.append(InlineKeyboardButton(
            text=str(page), callback_data=PageCallback(page_id=i).pack()))
    inline_keyboard.append(pages_row)
    inline_keyboard.append([
        InlineKeyboardButton(
            text="⬅️", callback_data=PrevOrNextCallback(direction="prev").pack()),
        InlineKeyboardButton(
            text="➡️", callback_data=PrevOrNextCallback(direction="next").pack())
    ],)
    inline_keyboard.append([
        InlineKeyboardButton(
            text="Меню", callback_data="menu")
    ])

    return InlineKeyboardMarkup(row_width=min(
        2, len(inline_keyboard[0])), inline_keyboard=inline_keyboard)
