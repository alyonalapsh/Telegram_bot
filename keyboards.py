from aiogram import types
from datetime import timedelta, datetime
import datetime as DT
import locale
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

import utilities

locale.setlocale(locale.LC_ALL, 'ru_RU')


# кнопка для выбора услуг
def keyboard_service():
    buttons = [
        [types.InlineKeyboardButton(text="Всё включено", callback_data="ch_all_include")],
        [types.InlineKeyboardButton(text="Наращивание", callback_data="ch_extensions")],
        [types.InlineKeyboardButton(text="Маникюр без покрытия", callback_data="ch_uncoated")],
        [types.InlineKeyboardButton(text="Френч/Градиент", callback_data="ch_design")],
        [types.InlineKeyboardButton(text="Подтвердить", callback_data="ch_finish")]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


# кнопки расписания
def keyboard_choose_date(page):
    buttons = []
    today = datetime.now()
    for days in range(page, page+7):  # 7 дней
        delta_time = (today + timedelta(days)).strftime("%a, %d %B")
        time_len = len(utilities.read_csv_time(delta_time))
        if time_len < 21:
            buttons.append([types.InlineKeyboardButton(text=delta_time, callback_data='book_date_' + delta_time)])
    if not page:
        buttons.append([types.InlineKeyboardButton(text="дальше", callback_data="level_next")])
    elif page == 21:
        buttons.append([types.InlineKeyboardButton(text="назад", callback_data="level_back")])
    else:
        buttons.append([types.InlineKeyboardButton(text="дальше", callback_data="level_next")])
        buttons.append([types.InlineKeyboardButton(text="назад", callback_data="level_back")])

    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


# кнопки времени
def keyboard_choose_time(date):
    builder = InlineKeyboardBuilder()
    step = DT.timedelta(minutes=30)
    date_fmt = '%H:%M'
    start = DT.datetime.strptime('10:00', date_fmt)

    for t in range(21):  # 21 кнопка
        time = start.strftime(date_fmt)
        if time not in utilities.read_csv_time(date):
            builder.button(text=time, callback_data='book_time_' + time)
        start += step

    builder.button(text='Назад к выбору даты', callback_data='ch_finish')
    builder.adjust(3)
    return builder.as_markup()


# кнопка подтверждения записи
def keyboard_end_of_book():
    buttons = [[types.InlineKeyboardButton(text="Подтвердить", callback_data="finish_book")],
              [types.InlineKeyboardButton(text="Назад к выбору даты", callback_data="ch_finish")]]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def keyboard_request_contact():
    builder = ReplyKeyboardBuilder()
    builder.add(
        types.KeyboardButton(text="Запросить контакт", request_contact=True, one_time_keyboard=True)
    )
    return builder
