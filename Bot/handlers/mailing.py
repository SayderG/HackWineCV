import asyncio
from aiogram import Dispatcher
from aiogram.types import Message


async def audience(messege: Message):
    pass

async def mailing(message: Message):
    config = message.bot.get('config')
    workers = config.bot.worker_ids
    for worker in workers:
        await message.bot.send_message(worker, message.text.split('mailing')[-1])


def register_start(dp: Dispatcher):
    dp.register_message_handler(mailing, commands=["mailing"], state="*")
