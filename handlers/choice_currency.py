from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from states.user_state import UserState
from keyboards.keyboards import get_reply_keyboard
from keyboards.keyboards import get_inline_keyboard
from keyboards.keyboards import CurrencyCallbackFactory
from calculation import calculation
from datetime import datetime


router = Router()


# State - None
@router.callback_query(StateFilter(None))
async def callbacks_without_state(callback: CallbackQuery):
    await callback.answer(text='Вернитесь в основное меню')


# State - choosing_first_currency, CurrencyCallbackFactory.filter - для проверки фабрики колбэков
@router.callback_query(UserState.choosing_first_currency, CurrencyCallbackFactory.filter(F.action == 'choice'))
async def callbacks_first_currency_chosen(callback: CallbackQuery, callback_data: CurrencyCallbackFactory, state: FSMContext):
    # print(f'Первая валюта - {callback_data.currency}')
    # записываем данные в хранилище FSM
    await state.update_data(chosen_currency=callback_data.currency)

    # Пока валюты получаем из словаря. Может быть потом будет список.
    buttons = {}
    for key, value in calculation.get_currencies().items():
        buttons.update({f'{key} - {value}': {
            'action': 'choice',
            'currency': key
        }})
    keyboard = get_inline_keyboard(buttons, [2])
    await callback.message.answer(text=f'Первая валюта <b>{callback_data.currency}</b>\nВыберите вторую валюту:', reply_markup=keyboard)
    # TODO Добавить вторую кнопку "Возврат" на ReplyKeyboard
    # Устанавливаем пользователю состояние 'choosing_second_currency'
    await state.set_state(UserState.choosing_second_currency)

    await callback.answer()


# State - choosing_first_currency, CurrencyCallbackFactory.filter - для проверки фабрики колбэков
@router.callback_query(UserState.choosing_second_currency, CurrencyCallbackFactory.filter(F.action == 'choice'))
async def callbacks_second_currency_chosen(callback: CallbackQuery, callback_data: CurrencyCallbackFactory, state: FSMContext):
    currency_data = await state.get_data()
    first_currency = currency_data['chosen_currency']
    # print(f'{first_currency = }')
    second_currency = callback_data.currency
    # print(f'{second_currency = }')

    if first_currency == second_currency:
        course = 1
    else:
        course = 'скоро получим из API'
    await callback.message.answer(text=f'На {datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}\n<b>Курс {first_currency} / {second_currency} = {course}</b>')
    # очистка State
    await state.clear()

    await callback.answer()


# TODO Добавить описание функций