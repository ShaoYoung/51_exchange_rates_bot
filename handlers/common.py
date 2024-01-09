from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove
from states.user_state import UserState
from keyboards.keyboards import get_reply_keyboard
from keyboards.keyboards import get_inline_keyboard
from calculation import calculation


router = Router()


@router.message(StateFilter(None), Command(commands=['start', 'Start', 'старт', 'Старт']))
async def cmd_start(message: Message, state: FSMContext):
    """
    Команда 'Start'. State не установлен.
    :param message: сообщение
    :param state: текущий статус
    :return: None
    """
    keyboard = get_reply_keyboard(['Возврат в основное меню'], [1])
    await message.answer(text='Я знаю курсы валют.', reply_markup=keyboard)

    # Пока валюты получаем из словаря. Может быть потом будет список.
    buttons = {}
    for key, value in calculation.get_currencies().items():
        buttons.update({f'{key} - {value}': {
            'action': 'choice',
            'currency': key
        }})
    keyboard = get_inline_keyboard(buttons, [2])
    await message.answer(text='Выберите первую валюту:', reply_markup=keyboard)
    # Устанавливаем пользователю состояние 'choosing_first_currency'
    await state.set_state(UserState.choosing_first_currency)


@router.message(F.text == 'Возврат в основное меню')
async def return_in_main_menu(message: Message, state: FSMContext):
    """
    Возврат в основное меню
    :param message: сообщение
    :param state: текущий статус
    :return: None
    """
    # очистка State
    await state.clear()
    await cmd_start(message, state)


@router.message(F.text.startswith(''))
async def cmd_incorrectly(message: Message):
    """
    Обработчик всех неизвестных команд
    :param message: сообщение
    :return: None
    """
    await message.reply(f'Я не знаю команду <b>"{message.text}"</b>')
    await message.answer('Пожалуйста, повторите ввод или нажмите кнопку ниже')


# TODO сделать Reply кнопку для возврата на шаг назад (доступно после выбора первой валюты)

