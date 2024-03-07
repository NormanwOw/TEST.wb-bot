from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from database.orm import database
from services import Response, WBService
from keyboards.inline_kb import get_sub_kb, get_cancel_kb, get_pagination_kb
from states import ProductState
from utils.storage import Storage
import messages
from config import bot

router = Router()
resp = Response()
wb = WBService()


@router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.delete()
    await message.answer(messages.START_MSG, parse_mode='HTML')


@router.message(Command('get_product'))
async def get_product(message: types.Message, state: FSMContext):
    await message.delete()
    await message.answer('Введите артикул', reply_markup=get_cancel_kb())
    await state.set_state(ProductState.product_id)


@router.message(Command('get_queries'))
async def get_queries(message: types.Message):
    await message.delete()
    msg = await resp.get_queries_msg(message.from_user.id)
    await message.answer(msg)


@router.callback_query(F.data.contains('stop'))
async def stop_mailing(callback: types.CallbackQuery):
    await callback.answer('Рассылка остановлена', show_alert=True)
    mailing_id = int(callback.data.split('_')[1])
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    await database.delete_mailing(callback.from_user.id, mailing_id)


@router.callback_query(F.data == 'sub')
async def start_mailing(callback: types.CallbackQuery):
    storage = Storage(callback.from_user.id)
    data = await storage.get()
    msg = data['msg']
    product_id = data['product_id']
    mailing = await database.get_mailing(callback.from_user.id, product_id)

    if mailing:
        return await callback.answer(messages.MAILING_EXISTS_MSG, show_alert=True)

    await callback.answer(messages.START_MAILING_MSG, show_alert=True)
    await database.add_mailing(callback.from_user.id, msg, product_id)


@router.callback_query(F.data.contains('prev') | F.data.contains('next'))
async def pagination_mailings(callback: types.CallbackQuery):
    action, page = callback.data.split('_')
    page = int(page)

    if page < 0:
        return await callback.answer()

    mailings = await database.get_mailings(callback.from_user.id)

    if page >= len(mailings):
        return await callback.answer()

    msg = mailings[page].message
    mailing_id = mailings[page].id
    await bot.edit_message_text(
        text=msg,
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=get_pagination_kb(
            mailing_id=mailing_id,
            count=len(mailings),
            page=page)
    )

    await callback.answer()


@router.message(Command('stop_mailing'))
async def stop_mailing(message: types.Message):
    await message.delete()
    mailings = await database.get_mailings(message.from_user.id)
    if not mailings:
        return message.answer('Список рассылок пуст')
    mailing = mailings[0]
    await message.answer(
        text=mailing.message,
        reply_markup=get_pagination_kb(mailing.id, count=len(mailings))
    )


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
        msg = await wb.get_product_msg(product_id)
        await message.answer(msg, reply_markup=get_sub_kb())
        await database.set_query(message.from_user.id, product_id)
        storage = Storage(message.from_user.id)
        await storage.set(product_id, msg)
        return await state.clear()
    except ValueError:
        answer = 'Неверный ввод'
    except TelegramBadRequest:
        answer = 'Товар не найден'

    await message.answer(answer, reply_markup=get_cancel_kb())

