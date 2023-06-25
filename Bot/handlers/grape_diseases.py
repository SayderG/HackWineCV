from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery

from Bot.keyboards.inline.grape import grape_markup
from Bot.misc.grape_texts import grade_ill_info, grade_causes_info
from leaves import get_leaves_predict


async def get_image(message: Message):
    processing = await message.answer("Обработка изображения")
    photo = message.photo[-1]
    file_info = await message.bot.get_file(photo.file_id)
    photo_path = f"src/leaves/{photo.file_unique_id}.jpg"
    await message.bot.download_file(file_info.file_path, photo_path)
    pred, text = get_leaves_predict(photo_path)
    await message.bot.edit_message_text(f"Предположительно это - {text}\nМожно узнать подробную информацию ниже",
                                        processing.chat.id,
                                        processing.message_id, reply_markup=grape_markup(pred))


async def get_info(callback_query: CallbackQuery):
    labels = {0: 'Черной гнили', 1: 'Эске', 2: 'Здоровом ростении', 3: 'Листовой гнили'}
    pred = callback_query.data.split(":")[-1]
    await callback_query.message.answer(f"Подробная информация о {labels[int(pred)]}\n{grade_ill_info[int(pred)]}")


async def get_causes(callback_query: CallbackQuery):
    labels = {0: 'Черной гнили', 1: 'Эски', 2: 'Здорового ростения', 3: 'Листовой гнили'}
    pred = callback_query.data.split(":")[-1]
    await callback_query.message.answer(f"Причины {labels[int(pred)]}\n{grade_causes_info[int(pred)]}")


def register_grape(dp: Dispatcher):
    dp.register_message_handler(get_image, content_types=['photo'], state="*")
    dp.register_callback_query_handler(get_info, lambda c: c.data.startswith("get_add_info"), state="*")
    dp.register_callback_query_handler(get_causes, lambda c: c.data.startswith("causes"), state="*")
