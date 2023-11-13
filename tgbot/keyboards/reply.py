from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from tgbot.misc.i18n import i18ns

_ = i18ns.gettext
languages_kb_text = ["🇺🇿 O'zbek", "🇷🇺 Русский"]
accepts_kb_text = [_("✅ Tasdiqlash")]
back_kb_text = _("🔙 Ortga")
cancel_kb_text = _("❌ Bekor qilish")


def back_kb():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add((KeyboardButton(text=back_kb_text)))
    return keyboard


def language_kb():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for language in languages_kb_text:
        keyboard.add((KeyboardButton(text=language)))
    return keyboard


def name_kb():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for option in accepts_kb_text:
        keyboard.add((KeyboardButton(text=cancel_kb_text)))
    return keyboard


def cancel_kb():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text=cancel_kb_text))
    return keyboard


def main_menu_kb():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    key1 = KeyboardButton(text=_("🔎 Tovar ID sini kiritish"))
    key2 = KeyboardButton(text=_("💰 Mening keshbeklarim"))
    key3 = KeyboardButton(text=_("🛒 Buyurtma berish"))
    key4 = KeyboardButton(text=_("⌛️ Sotuvlar tarixi"))
    key5 = KeyboardButton(text=_("📞 Aloqa"))
    key6 = KeyboardButton(text=_("⚙️ Sozlamalar"))
    key7 = KeyboardButton(text=_("🆘 Feedback"))
    keyboard.add(key1)
    keyboard.add(key2, key3)
    keyboard.add(key4, key5)
    keyboard.add(key6, key7)
    return keyboard
