from aiogram import Router, types
from aiogram.filters import CommandStart, Command

from services import Response
from keyboards.inline_kb import get_sub_kb

router = Router()
resp = Response()


@router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer('Старт')
    await message.delete()


@router.message(Command('get_product'))
async def get_product(message: types.Message):
    pass


@router.message(Command('get_queries'))
async def get_queries(message: types.Message):
    msg = await resp.get_queries_msg(message.from_user.id)
    await message.answer(msg, reply_markup=get_sub_kb())


@router.message(Command('stop_mailing'))
async def stop_mailing(message: types.Message):
    pass
