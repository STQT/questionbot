import logging
import pytz
from datetime import datetime
from aiogram import types, Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiohttp import ClientError, ClientResponseError

from tgbot.db.queries import Database
from tgbot.keyboards.reply import cancel_kb
from tgbot.misc.states import AddChannel


def choices_kb(poll, choices: list):
    inline_keyboard = []
    for choice in choices:
        inline_keyboard.append(
            [InlineKeyboardButton(text=f"{choice['text']}", callback_data=str(poll) + ":" + str(choice['id']))])
    markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return markup


def channels_keyboard(channels, poll_pk):
    inline_keyboard = []
    for channel in channels:
        channel_link = channel['link']
        channel_link = "https://t.me/" + channel_link if channel_link.startswith("@") else channel_link
        inline_keyboard.append([InlineKeyboardButton(text=channel['name'], url=channel_link)])
    inline_keyboard.append([InlineKeyboardButton(text="A'zo bo'ldim", callback_data="submit_channel:" + str(poll_pk))])
    markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return markup


async def check_user_subscription(bot: Bot, chat_id, user_id):
    try:
        chat_member = await bot.get_chat_member(chat_id, user_id)
        if chat_member.status in ['member', 'administrator', 'creator']:
            return True
        else:
            return False
    except Exception as e:
        logging.exception(e)
        return False


async def user_subscription_msg(bot, chat_id_list, user_id):
    unsubscribed_channel_list = []
    for chat in chat_id_list:
        is_subscribed = await check_user_subscription(bot, chat['channel_id'], user_id)
        if is_subscribed is False:
            unsubscribed_channel_list.append(chat)
    return unsubscribed_channel_list


async def check_subscriber_with_poll_id(m: types.Message, db: Database, poll, user_id):
    poll_id = poll['id']
    channel_list = await db.get_poll_owner_channels(poll_id)
    unsubscribed_channel_list = await user_subscription_msg(m.bot, channel_list, user_id)
    if unsubscribed_channel_list:
        return await m.answer("Ushbu botdan foydalanish uchun quyidagi kanallarga a'zo bo'lish kerak",
                              reply_markup=channels_keyboard(unsubscribed_channel_list, poll_id))
    return await m.answer(poll['text'].replace("<br />", "\n"),
                          reply_markup=choices_kb(poll_id, poll['choices']),
                          parse_mode="HTML")


async def main_start_handler(m: types.Message, state: FSMContext, db: Database):
    args: str = m.get_args()
    if args.startswith("channel"):
        _channel, guid = args.split("channel")
        await m.answer("Kanalni platformaga qo'shish uchun quyidagi amallarni bajaring:\n"
                       "1. Kanalga ushbu botni qo'shing\n"
                       "2. Kanaldan biron bir xabarni ushbu botga yo'naltiring (переслать)", reply_markup=cancel_kb())
        await AddChannel.get_channel_msg.set()
        await state.update_data(guid=guid)
    elif args.startswith("poll"):
        poll_id = args.split("poll")[1]
        try:
            poll = await db.get_poll(poll_id)
            tashkent_tz = pytz.timezone('Asia/Tashkent')
            dt = datetime.strptime(poll['closed_at'][:-6], '%Y-%m-%dT%H:%M:%S')
            localized_dt = tashkent_tz.localize(dt)
            current_time_tashkent = datetime.now(tashkent_tz)
            if localized_dt < current_time_tashkent:
                await m.answer("Savol ovoz berish vaqti tugagan")
            else:
                await check_subscriber_with_poll_id(m, db, poll, m.from_user.id)
        except ClientResponseError:
            await m.answer("Server bilan bog'lanishda xato sodir bo'ldi.")
        except ClientError:
            await m.answer("Savol topilmadi.")
    else:
        await m.answer("Bot test rejimida ishlayapti", reply_markup=types.ReplyKeyboardRemove())


async def submit_subscribe(call: types.CallbackQuery, db: Database):
    await call.answer("Tanlandi")
    _submit_channel, poll_id = call.data.split(":")
    await call.message.delete()
    poll = await db.get_poll(poll_id)
    await check_subscriber_with_poll_id(call.message, db, poll, call.from_user.id)


async def submit_vote(call: types.CallbackQuery, db: Database):
    await call.answer("Tanlandi")
    poll, choice = call.data.split(":")
    try:
        vote, is_voted = await db.vote(user_id=call.from_user.id, poll_id=poll, choice=choice)
        await call.message.delete()
        if is_voted:
            await call.message.answer(f"Sizning ovozingiz <b>{vote['choice_text']}</b> javobga qabul qilindi", parse_mode="HTML")
        else:
            await call.message.answer(vote['poll'][-1], parse_mode="HTML")
    except ClientError:
        await call.message.answer("Server bilan bog'lanishda xato sodir bo'ldi birozdan so'ng xarakat qilib ko'ring")


def register_start(dp: Dispatcher):
    dp.register_message_handler(main_start_handler, commands=['start'])
    dp.register_callback_query_handler(submit_subscribe, lambda c: c.data.startswith('submit_channel:'))
    dp.register_callback_query_handler(submit_vote)
