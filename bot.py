import os

import asyncio
import logging

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, StateFilter

import my_command
import callbacks
from my_command import UserState
import data_to_csv

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
token = os.environ['TOKEN']
bot = Bot(token=token)
# Диспетчер
dp = Dispatcher(storage=MemoryStorage())

dir_name = 'resources/'

file_name_clients_data = "clients_data.csv"
file_path_clients_data = dir_name + file_name_clients_data

file_name_unavailable_time = "unavailable_time.csv"
file_path_unavailable_time = dir_name + file_name_unavailable_time

data_to_csv.create_csv_file(file_path_clients_data, file_name_clients_data)
data_to_csv.create_csv_file(file_path_unavailable_time, file_name_unavailable_time)


# команда старт
dp.message.register(my_command.cmd_start, Command("start"), StateFilter(None))

# декоратор кнопку записаться
dp.callback_query.register(callbacks.book_client, F.data == "book", StateFilter(None))

# декоратор на кнопку мои записи
dp.callback_query.register(callbacks.show_client_booking, F.data == "check", StateFilter(None))

# декоратор кнопок выбора услуг
dp.callback_query.register(
    callbacks.callbacks_service, F.data.startswith("ch_"),
    StateFilter(UserState.choosing_service, UserState.choosing_date, UserState.choosing_time, UserState.finish_book)
)

# декоратор кнопок перелистывания дат
dp.callback_query.register(callbacks.edit_level, F.data.startswith("level_"), StateFilter(UserState.choosing_date))

# декоратор выбора даты
dp.callback_query.register(
    callbacks.callback_date, F.data.startswith("book_date_"), StateFilter(UserState.choosing_date)
)

# декоратор выбора времени
dp.callback_query.register(
    callbacks.callback_time, F.data.startswith("book_time_"), StateFilter(UserState.choosing_time)
)

# декоратор подтверждения записи
dp.callback_query.register(callbacks.finish_book, F.data == "finish_book", StateFilter(UserState.finish_book))

# декоратор на сообщение с номером телефона
dp.message.register(callbacks.on_contact_shared, F.contact, StateFilter(UserState.finish_book))


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())




