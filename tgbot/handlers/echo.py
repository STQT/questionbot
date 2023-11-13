import logging

from aiogram import types, Dispatcher
from tgbot.db.queries import Database


async def bot_echo_all(m: types.Message, db: Database):
    await m.answer("Ushbu botdan foydalanish uchun https://questionbot.itlink.uz dan ro'yxatdan o'ting")


# state_name = await state.get_state()
# text = [
#     f'Эхо в состоянии {hcode(state_name)}',
#     'Содержание сообщения:',
#     hcode(message.text)
# ]
# await message.answer('\n'.join(text))


def register_echo(dp: Dispatcher):
    dp.register_message_handler(bot_echo_all, state="*", content_types=types.ContentTypes.ANY)
