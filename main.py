import asyncio
import os.path

from database.creator import create_database
from json_checker import read_config

data = read_config()

if not os.path.exists(data["database_path"]):
    create_database(data["database_path"])

from aiogram import Dispatcher, Bot

from routers.api_loginer import router as login_router
from routers.enter import router as enter_router
from routers.imei_checker import router as checker_router

dp = Dispatcher()
dp.include_router(login_router)
dp.include_router(enter_router)
dp.include_router(checker_router)

bot = Bot(token=data["bot_token"])


async def run():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(run())
