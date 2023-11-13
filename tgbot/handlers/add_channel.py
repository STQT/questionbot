import logging

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentTypes
from aiogram.utils.exceptions import Unauthorized
from aiohttp import ClientResponseError, ClientError, ClientSession

from tgbot.db.queries import Database
from tgbot.misc.states import AddChannel



async def get_channel_msg(m: types.Message, db: Database, state: FSMContext):
    data = await state.get_data()
    if m.is_forward() and m.forward_from_chat.type == "channel" and 'guid' in data:
        try:
            await m.send_copy(m.from_user.id)
            await m.bot.get_chat_administrators(m.forward_from_chat.id)
            try:
                await db.create_channel(data['guid'], str(m.forward_from_chat.id), m.forward_from_chat.title)
                await m.answer("Sizning kanalingiz platformaga qo'shildi")
                await state.finish()
            except ClientResponseError:
                await m.answer("Server bilan bog'lanishdagi xato, birozdan so'ng urunib ko'ring")
            except Database.ChannelAlreadyExists:
                await m.answer("Ushbu kanal allaqachon qo'shilgan")

        except Unauthorized:
            await m.answer("Ushbu bot kanalda admin sifatida qayd etilmagan, "
                           "iltimos kanalga admin sifatida qo'shib keyin kanaldan xabaringizni yo'naltiring")
    elif 'guid' not in data:
        await m.answer("Platformadan qaytadan kanal yaratish tugmasini bosing, bog'lanish uzildi.")
    else:
        await m.answer("Iltimos menga kanal nomidan yo'naltirilgan postni yuboring")


def register_add_channel_handlers(dp: Dispatcher):
    dp.register_message_handler(get_channel_msg, state=AddChannel.get_channel_msg, content_types=ContentTypes.ANY)
