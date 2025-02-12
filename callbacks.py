from aiogram import types
from aiogram.fsm.context import FSMContext

import keyboards
import utilities
from my_command import UserState


# хэндлер на кнопку записаться
async def book_client(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "Выберите услуги:",
        reply_markup=keyboards.keyboard_service()
    )
    await state.set_state(UserState.choosing_service)


# хэндлер на услуги
async def callbacks_service(callback: types.CallbackQuery, state: FSMContext):
    action = callback.data[3:]
    data = await state.get_data()

    if action == "all_include":
        data['chosen_service'].append("Всё включено")
        await utilities.update_book(callback.message, state)

    elif action == "extensions":
        data['chosen_service'].append("Наращивание")
        await utilities.update_book(callback.message, state)

    elif action == "uncoated":
        data['chosen_service'].append("Маникюр без покрытия")
        await utilities.update_book(callback.message, state)

    elif action == "design":
        data['chosen_service'].append("Френч/Градиент")
        await utilities.update_book(callback.message, state)

    elif action == "finish":
        await utilities.choose_date(callback.message, state)


# хэндлер на кнопки дальше и назад
async def edit_level(callback: types.CallbackQuery, state: FSMContext):
    await utilities.edit_schedule(callback.message, callback.data, state)


# хэндлер на выбор даты
async def callback_date(callback: types.CallbackQuery, state: FSMContext):
    await utilities.choose_time(callback.message, callback.data, state)


# хэндлер на выбор времени
async def callback_time(callback: types.CallbackQuery, state: FSMContext):
    await utilities.confirm_book(callback.message, callback.data, state)


# хэндлер на конец записи
async def finish_book(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    await state.update_data(user_id=user_id)
    await utilities.show_book_info(callback.message, state)


async def on_contact_shared(message: types.Message, state: FSMContext):
    await utilities.on_contact_shared(message, state)


async def show_client_booking(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await utilities.show_client_book(callback.message, user_id)
