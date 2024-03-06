from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command

from database.orm import database
from services import Response, WBService
from keyboards.inline_kb import get_sub_kb
import messages

router = Router()
resp = Response()
wb = WBService()


@router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.delete()
    await message.answer(messages.START_MSG)


@router.message(Command('get_product'))
async def get_product(message: types.Message):
    # await message.delete()
    msg = await wb.get_product_msg(message.from_user.id, 211695539)
    await message.answer(msg)


@router.message(Command('get_queries'))
async def get_queries(message: types.Message):
    # await message.delete()
    msg = await resp.get_queries_msg(message.from_user.id)
    await message.answer(msg, reply_markup=get_sub_kb())


@router.message(Command('stop_mailing'))
async def stop_mailing(message: types.Message):
    # await message.delete()
    await database.delete_mailing(message.from_user.id)
    await message.answer(messages.STOP_MAILING_MSG)


@router.callback_query(F.data == 'sub')
async def start_mailing(callback: types.CallbackQuery):
    await database.add_mailing(callback.from_user.id)
    await callback.answer(messages.START_MAILING_MSG)
