from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from tgbot.db.queries import Database
from tgbot.handlers.register import register_start_message
from tgbot.keyboards.reply import main_menu_kb, back_kb
from tgbot.misc.states import MainMenuState


async def main_menu_handler(m: types.Message, state: FSMContext, db: Database):
    if m.text in ["📞 Aloqa", "⚙️ Sozlamalar", "🆘 Feedback"]:
        await m.answer("Ushbu bo'lim ishlab chiqish jarayonda")
    else:
        await m.answer(m.text, reply_markup=main_menu_kb())


def register_menu(dp: Dispatcher):
    dp.register_message_handler(main_menu_handler, state=MainMenuState.get_menu, content_types=types.ContentTypes.ANY)
