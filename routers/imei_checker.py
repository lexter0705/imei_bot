import aiohttp
from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from database.worker import UserWorker
from json_checker import read_config

router = Router()

data = read_config()
worker = UserWorker(data["database_path"])


class ImeiStates(StatesGroup):
    imei = State()


@router.callback_query(F.data == "imei")
async def check_imei(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(ImeiStates.imei)
    await callback.message.reply("Enter imei:")


@router.message(ImeiStates.imei)
async def check_imei(message: types.Message, state: FSMContext):
    await state.set_state()
    imei = message.text
    async with aiohttp.ClientSession() as session:
        api_key = worker.get_api_key(message.from_user.id)
        async with session.post(f"{data['api_link']}/check_imei", json={"api_key": api_key, "imei": imei}) as response:
            await message.reply(str(await response.json()))
