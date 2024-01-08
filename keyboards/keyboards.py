from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData


class CurrencyCallbackFactory(CallbackData, prefix="currency"):
    action: str
    currency: str


def get_reply_keyboard(buttons_text: list, adjust: list, resize_keyboard: bool = True, one_time_keyboard: bool = False) -> ReplyKeyboardMarkup:
    """
    Создаёт ReplyKeyboard
    :param buttons_text: текст на кнопках
    :param adjust: количество кнопок по рядам
    :param resize_keyboard: автоматическое изменение клавиатуры под экран
    :param one_time_keyboard: автоматическое скрытие клавиатуры после нажатия кнопки
    :return: ReplyKeyboardMarkup
    """
    builder = ReplyKeyboardBuilder()
    for button_text in buttons_text:
        builder.button(text=button_text)
    builder.adjust(*adjust)
    return builder.as_markup(resize_keyboard=resize_keyboard, one_time_keyboard=one_time_keyboard)


def get_inline_keyboard(buttons: dict, adjust: list) -> InlineKeyboardMarkup:
    """
    Создаёт InlineKeyboard
    :param buttons: кнопки с коллбэком (фабрика коллбэков)
    :param adjust: количество кнопок по рядам
    :return: InlineKeyboardMarkup
    """
    builder = InlineKeyboardBuilder()
    for key, value in buttons.items():
        builder.button(text=key, callback_data=CurrencyCallbackFactory(action=value['action'], currency=value['currency']))
    builder.adjust(*adjust)
    return builder.as_markup()

