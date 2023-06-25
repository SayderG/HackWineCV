from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def grape_markup(pred):
    grape_btn_1 = InlineKeyboardButton("Подробнее", callback_data=f"get_add_info:{pred}")
    grape_btn_2 = InlineKeyboardButton("Причины возникновения", callback_data="get_image")
    grape_btn_3 = InlineKeyboardButton("Назад", callback_data="back")
    markup = InlineKeyboardMarkup(row_width=1).add(grape_btn_1, grape_btn_2, grape_btn_3)
    return markup
