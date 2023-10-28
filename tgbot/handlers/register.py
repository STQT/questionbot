from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from tgbot.keyboards.reply import main_menu_kb, language_kb, languages_kb_text, name_kb, accepts_kb_text
from tgbot.misc.states import UserRegisterState


async def register_start_message(message: types.Message, state: FSMContext):
    await message.answer(
        "Выберите свой язык\n"
        "Sizga qulay tilni tanlang\n"
        "Choose your language",
        reply_markup=language_kb())
    await state.set_state(UserRegisterState.get_lang)


async def get_lang_handler(message: types.Message, state: FSMContext):
    if message.text in languages_kb_text:
        await state.update_data(lang=message.text)
        await message.answer(f'{message.from_user.full_name}, iltimos, ismingiz kiriting yoki tasdiqlang👇',
                             reply_markup=name_kb())
        await state.set_state(UserRegisterState.get_name)
    else:
        await message.answer("Iltimos, tugmadan tilni tanlang 👇", reply_markup=language_kb())


async def get_name_handler(message: types.Message, state: FSMContext):
    if message.text in accepts_kb_text:
        await state.update_data(name=message.from_user.full_name)
    else:
        await state.update_data(name=message.text)
    await message.answer("Iltimos, do'kon nomini kiriting",
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(UserRegisterState.get_organization_name)


async def get_org_name_handler(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.finish()
    await message.answer("Kategoriyani tanlang", reply_markup=main_menu_kb())


def register_register(dp: Dispatcher):
    dp.register_message_handler(register_start_message, state=UserRegisterState.send_question,
                                content_types=types.ContentTypes.TEXT)
    dp.register_message_handler(get_lang_handler, state=UserRegisterState.get_lang,
                                content_types=types.ContentTypes.TEXT)
    dp.register_message_handler(get_name_handler, state=UserRegisterState.get_name,
                                content_types=types.ContentTypes.TEXT)
    dp.register_message_handler(get_org_name_handler, state=UserRegisterState.get_organization_name,
                                content_types=types.ContentTypes.TEXT)
