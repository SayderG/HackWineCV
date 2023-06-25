import asyncio
from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery


async def main_message(message: Message):
    await message.answer("Отправь мне фотографию листа")


async def callback_main_message(callback_query: CallbackQuery):
    await callback_query.message.answer("Отправь мне фотографию листа")


async def start_message(message: Message):
    await main_message(message)


def register_start(dp: Dispatcher):
    dp.register_message_handler(start_message, commands=["start"], state="*")
    dp.register_callback_query_handler(callback_main_message, lambda c: c.data == "back", state="*")
