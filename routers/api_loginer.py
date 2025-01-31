import aiohttp
from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from database.worker import UserWorker
from json_checker import read_config

router = Router()

data = read_config()
worker = UserWorker(data["database_path"])


class LoginStates(StatesGroup):
    api_key = State()


@router.callback_query(F.data == "apikey")
async def enter_api_key(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(LoginStates.api_key)
    await callback.message.reply("Enter api key:")


@router.message(LoginStates.api_key)
async def check_api_key(message: types.Message, state: FSMContext):
    await state.set_state()
    api_key = message.text
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{data['api_link']}/check_api_key", json={"api_key": api_key}) as response:
            if response.status == 200:
                worker.add_user(message.from_user.id, api_key)
                await message.reply("API key is valid.")
            else:
                await message.reply("Uncorrect api key")
