from aiogram.dispatcher.filters.state import StatesGroup, State


class UserRegisterState(StatesGroup):
    send_question = State()
    get_lang = State()
    get_name = State()
    get_organization_name = State()


class MainMenuState(StatesGroup):
    get_menu = State()


class AddChannel(StatesGroup):
    get_channel_msg = State()