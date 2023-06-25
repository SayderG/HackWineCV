import asyncio
from aiogram import Dispatcher
from aiogram.types import Message


async def main_message(message: Message):
    await message.answer("Отправь мне фотографию листа")


async def start_message(message: Message):
    await main_message(message)


def register_start(dp: Dispatcher):
    dp.register_message_handler(start_message, commands=["start"], state="*")
