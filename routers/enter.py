import aiohttp
from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database.worker import UserWorker
from json_checker import read_config, read_white_list

router = Router()

data = read_config()
white_list = read_white_list()
worker = UserWorker(data["database_path"])


@router.message(CommandStart())
async def answer_start(message: types.Message):
    text = "You can't use the bot."
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Enter by api key",
                                                                           callback_data="apikey")]])

    if worker.is_user(message.from_user.id):
        text = "You can start use bot!"
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Check imei",
                                                                               callback_data="imei")]])

    elif message.from_user.id in white_list:
        text = "You can start use bot!"
        await register(message.from_user.id)
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Check imei",
                                                                               callback_data="imei")]])

    await message.reply(f"Hello! I am bot fot check phone imei!\n{text}", reply_markup=keyboard)


async def register(user_id: int):
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{data['api_link']}/create_api_key",
                               json={"api_key": data["admin_api_key"]}) as response:
            api_key = await response.json()
    worker.add_user(user_id, api_key["new_key"])
