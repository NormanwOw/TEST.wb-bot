from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from database.orm import database
from services import Response, WBService
from keyboards.inline_kb import get_sub_kb, get_cancel_kb, get_pagination_kb
from states import ProductState
import messages
from config import bot

router = Router()
resp = Response()
wb = WBService()


@router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.delete()
    await message.answer(messages.START_MSG)


@router.message(Command('get_product'))
async def get_product_cmd(message: types.Message, state: FSMContext):
    await message.delete()
    await message.answer('Введите артикул', reply_markup=get_cancel_kb())
    await state.set_state(ProductState.product_id)


@router.message(Command('stop_mailing'))
async def stop_mailing_cmd(message: types.Message):
    await message.delete()

    mailings = await database.get_mailings(message.from_user.id)

    if not mailings:
        return message.answer(messages.EMPTY_MAILING_MSG)

    await message.answer(
        text=await resp.get_mailing_msg(mailings[0]),
        reply_markup=get_pagination_kb(mailings[0].id, count=len(mailings)),
    )


@router.message(Command('get_queries'))
async def get_queries_cmd(message: types.Message):
    await message.delete()
    msg = await resp.get_queries_msg(message.from_user.id)
    await message.answer(msg)


@router.callback_query(F.data.contains('stop'))
async def stop_mailing(callback: types.CallbackQuery):
    await callback.answer(messages.STOP_MAILING_MSG, show_alert=True)
    mailing_id = int(callback.data.split('_')[1])
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    await database.delete_mailing(mailing_id)


@router.callback_query(F.data == 'sub')
async def start_mailing(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    query_id = data['query_id']
    title = data['title']

    if await database.get_mailing(query_id):
        return await callback.answer(messages.MAILING_EXISTS_MSG, show_alert=True)

    await callback.answer(messages.START_MAILING_MSG, show_alert=True)
    await database.set_mailing(query_id, title)


@router.callback_query(F.data.contains('prev') | F.data.contains('next'))
async def pagination_mailings(callback: types.CallbackQuery):
    action, page = callback.data.split('_')
    page = int(page)

    if action == 'prev':
        page -= 1
    else:
        page += 1

    if page < 0:
        return await callback.answer()

    mailings = await database.get_mailings(callback.from_user.id)

    if page > len(mailings) - 1:
        return await callback.answer()

    mailing_id = mailings[page].id
    mailing = mailings[page]

    await bot.edit_message_text(
        text=await resp.get_mailing_msg(mailing),
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=get_pagination_kb(
            mailing_id=mailing_id,
            count=len(mailings),
            page=page),
    )

    await callback.answer()


@router.callback_query(F.data == 'cancel')
async def cancel_state(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer('Ввод отменён')
    await bot.delete_message(callback.from_user.id, callback.message.message_id)


@router.message(ProductState.product_id)
async def get_product_id(message: types.Message, state: FSMContext):
    await message.delete()
    try:
        product_id = int(message.text)
        msg, title = await wb.get_product(product_id)
        await message.answer(msg, reply_markup=get_sub_kb())
        query_id = await database.set_query(message.from_user.id, product_id)
        await state.clear()
        await state.set_data({'query_id': query_id, 'title': title})
        return
    except ValueError:
        answer = 'Неверный ввод'
    except TelegramBadRequest:
        answer = 'Товар не найден'

    await message.answer(answer, reply_markup=get_cancel_kb())

