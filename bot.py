import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.utils import executor
from aiogram.utils.executor import start_webhook

from tgbot.config import load_config
from tgbot.db.queries import Database
from tgbot.filters.admin import AdminFilter
from tgbot.handlers.add_channel import register_add_channel_handlers
from tgbot.handlers.echo import register_echo
from tgbot.handlers.menu import register_menu
from tgbot.handlers.register import register_register
from tgbot.handlers.start import register_start
from tgbot.middlewares.acl import ACLMiddleware
from tgbot.middlewares.environment import EnvironmentMiddleware

logger = logging.getLogger(__name__)

# webhook settings



def register_all_middlewares(dp, config, db):
    dp.setup_middleware(EnvironmentMiddleware(config=config, db=db))
    dp.setup_middleware(ACLMiddleware())


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    register_start(dp)
    register_add_channel_handlers(dp)
    register_menu(dp)
    register_register(dp)
    register_echo(dp)

logging.basicConfig(
    level=logging.INFO,
    format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
)
logger.info("Starting bot")
config = load_config(".env")

WEBHOOK_HOST = config.tg_bot.host
WEBHOOK_PATH = '/webhook'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
WEBAPP_HOST = '0.0.0.0'  # or ip
WEBAPP_PORT = 5000

storage = MemoryStorage()
if config.tg_bot.debug is False:
    import sentry_sdk
    from sentry_sdk.integrations.asyncio import AsyncioIntegration
    sentry_sdk.init(dsn=config.misc.sentry_dsn, integrations=[AsyncioIntegration()])
    storage = RedisStorage2(host="redis", port=6380, db=0)
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
dp = Dispatcher(bot, storage=storage)
bot['config'] = config

register_all_middlewares(dp, config,
                         db=Database(config.db.base_url))
register_all_filters(dp)
register_all_handlers(dp)

async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(dp):
    logging.warning('Shutting down..')
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning('Bye!')

if __name__ == '__main__':
    executor.start_polling(dp, on_shutdown=on_shutdown)
    # start_webhook(
    #     dispatcher=dp,
    #     webhook_path=WEBHOOK_PATH,
    #     on_startup=on_startup,
    #     on_shutdown=on_shutdown,
    #     skip_updates=True,
    #     host=WEBAPP_HOST,
    #     port=WEBAPP_PORT,
    # )
