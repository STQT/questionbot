import logging
from typing import Tuple, Any
from aiogram.contrib.middlewares.i18n import I18nMiddleware as BaseI18nMiddleware


class I18nMiddleware(BaseI18nMiddleware):
    async def get_user_locale(self, action: str, args: Tuple[Any]):
        data: dict = args[-1]
        try:
            return data['user_lang']
        except:
            return "uz"