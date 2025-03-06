from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

bot_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Добавить задачу для повторения")],
        [KeyboardButton(text="Просмотреть список добавленых задач")],
    ],
    resize_keyboard=True
)
