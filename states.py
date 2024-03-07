from aiogram.fsm.state import StatesGroup, State


class ProductState(StatesGroup):
    product_id = State()
