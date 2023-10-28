from tgbot.config import I18N_DOMAIN, LOCALES_DIR
from tgbot.middlewares.i18n import I18nMiddleware


i18ns = I18nMiddleware(domain=I18N_DOMAIN, path=LOCALES_DIR, default="uz")