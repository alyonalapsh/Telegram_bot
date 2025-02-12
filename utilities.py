from aiogram import types
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
import csv
import datetime as DT
import locale

import keyboards
import Client
from my_command import UserState
import data_to_csv

locale.setlocale(locale.LC_ALL, 'ru_RU')


# редактирование выбранных услуг
async def update_book(message: types.Message, state: FSMContext):
    with suppress(TelegramBadRequest):
        data = await state.get_data()
        user_service = '\n'.join(data["chosen_service"])
        await message.edit_text(
            "Выбранные услуги:" + "\n" + user_service,
            reply_markup=keyboards.keyboard_service()
        )


# показываются выбранные услуги и кнопка выбора даты
async def choose_date(message: types.Message, state: FSMContext):
    await state.update_data(page=0)
    data = await state.get_data()
    page = data["page"]
    user_services = '\n'.join(data["chosen_service"])
    with suppress(TelegramBadRequest):
        await message.edit_text(
            "Итого:" + "\n" + user_services,
            reply_markup=keyboards.keyboard_choose_date(page)
        )
    await state.set_state(UserState.choosing_date)


# редактор расписания
async def edit_schedule(message: types.Message, callback: str, state: FSMContext):
    data = await state.get_data()
    page = data["page"]
    page = page + 7 if callback[-4:] == "next" else page - 7

    await state.update_data(page=page)
    await message.edit_text(
        message.text,
        reply_markup=keyboards.keyboard_choose_date(page)
    )


# показывает выбор времени
async def choose_time(message: types.Message, callback: str, state: FSMContext):
    callback = callback[10:]
    await state.update_data(chosen_date=callback)
    data = await state.get_data()
    with suppress(TelegramBadRequest):
        await message.edit_text(
            "Вы выбрали: " + "\n" + '\n'.join(data["chosen_service"]) + "\n" + callback,
            reply_markup=keyboards.keyboard_choose_time(callback)
        )
    await state.set_state(UserState.choosing_time)


async def confirm_book(message: types.Message, callback: str, state: FSMContext):
    callback = callback[10:]
    await state.update_data(chosen_time=callback)
    with suppress(TelegramBadRequest):
        await message.edit_text(
            message.text + ' ' + callback,
            reply_markup=keyboards.keyboard_end_of_book()
        )
    await state.set_state(UserState.finish_book)


async def create_client_book(state: FSMContext):
    data = await state.get_data()
    client = Client.Client()

    client.set_client_id(data["user_id"])
    client.set_name(data["name"])
    client.set_phone_number(data["phone_number"])
    client.set_services(','.join(data["chosen_service"]))
    client.set_book_date(data["chosen_date"])
    client.set_book_time(data["chosen_time"])

    data_to_csv.add_book_client(client)
    data_to_csv.add_book_time(client)


async def show_book_info(message: types.Message, state: FSMContext):
    await message.edit_text(message.text)
    await get_client_contact(message)


async def get_client_contact(message: types.Message):
    await message.answer(
        text="Для завершения записи оставьте Ваш номер телефона:",
        reply_markup=keyboards.keyboard_request_contact().as_markup(resize_keyboard=True)
    )


async def on_contact_shared(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.contact.phone_number)
    await create_client_book(state)
    await message.answer("Спасибо за запись!", reply_markup=types.ReplyKeyboardRemove())
    await state.clear()


async def read_csv_file(client_id):
    file_name = "clients_data.csv"
    file_path = "resources/" + file_name
    client = Client.Client()
    book_info = []

    with open(file_path, 'r', encoding='utf-8', newline='') as csvfile:
        file_reader = csv.reader(csvfile)
        for row in file_reader:
            user_id, name, phone_number, services, book_date, book_time = row
            if user_id == str(client_id):
                client.set_client_id(user_id)
                client.set_name(name)
                client.set_phone_number(phone_number)
                client.set_services(services + ":")
                client.set_book_date("\n" + book_date)
                client.set_book_time(book_time)
                book_info.append(' '.join([client.get_services(), client.get_book_date(), client.get_book_time()]))
    return book_info


async def show_client_book(message: types.Message, user_id):
    book_info = await read_csv_file(user_id)
    book_info = '\n\n'.join(book_info)

    await message.answer(f"Ваши записи:\n{book_info}")


def generate_book_time(time):
    step = DT.timedelta(minutes=30)
    date_fmt = '%H:%M'
    start = DT.datetime.strptime(time, date_fmt)
    booked_time = [time]
    for i in range(3): # 3 недоступного времени
        start -= step
        booked_time.append(start.strftime(date_fmt))

    start = DT.datetime.strptime(time, date_fmt)
    for i in range(3):
        start += step
        booked_time.append(start.strftime(date_fmt))

    return ','.join(booked_time)


def read_csv_time(date):
    unavailable_time = set()
    with open("resources/unavailable_time.csv", 'r', encoding='utf-8', newline='') as csvfile:
        file_reader = csv.reader(csvfile)
        for row in file_reader:
            book_date, time = row
            if book_date == date:
                unavailable_time.update(time.split(","))

    return unavailable_time - {'08:30', '09:00', '09:30', '20:30', '21:00', '21:30'}
