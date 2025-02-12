from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

class UserState(StatesGroup):
    choosing_service = State()
    choosing_date = State()
    choosing_time = State()
    finish_book = State()

# начало записи
async def cmd_start(message: types.Message, state: FSMContext):

    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Записаться",
        callback_data="book")
    )
    builder.add(types.InlineKeyboardButton(
        text="Мои записи",
        callback_data="check")
    )
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    user_name = f'{first_name} {last_name}' if last_name else f'{first_name}'

    await state.update_data(name=user_name)
    await state.update_data(chosen_service=[])

    await message.answer(
        f"Привет, {user_name}! \nВыбери действие:",
        reply_markup=builder.as_markup()
    )
