from aiogram import Bot, Dispatcher, executor  #, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# from aiogram.dispatcher import FSMContext
# import asyncio

api = "myAPI"

bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
kb = ReplyKeyboardMarkup(resize_keyboard=True) #, one_time_keyboard=True)
button = KeyboardButton(text="Рассчитать")
button2 = KeyboardButton(text="Информация")
kb.row(button, button2)
kb.add(KeyboardButton(text="Купить"))

kb_in = InlineKeyboardMarkup(resize_keyboard=True)
button_in = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button2_in = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb_in.row(button_in, button2_in)

kb_menu = InlineKeyboardMarkup(resize_keyboard=True)
button_m1 = InlineKeyboardButton(text='Product1', callback_data='product_buying')
button_m2 = InlineKeyboardButton(text='Product2', callback_data='product_buying')
button_m3 = InlineKeyboardButton(text='Product3', callback_data='product_buying')
button_m4 = InlineKeyboardButton(text='Product4', callback_data='product_buying')
kb_menu.row(button_m1, button_m2, button_m3, button_m4)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот, помогающий твоему здоровью.', reply_markup=kb)


@dp.message_handler(text=['Купить'])
async def get_buying_list(message):
    tit = {1: 'Пекинский салат (16 к/кал)', 2: 'Редис (25 к/кал)', 3: 'Брокколи (34 к/кал)',
           4: 'Зеленый горошек (55 к/кал)'}
    for i in (1, 2, 3, 4):
        await message.answer(f'Название: Product{i} | Описание: {tit[i]} | Цена: {i * 100}')
        with open(f'photo/{i}.png', 'rb') as img:
            await message.answer_photo(img)

    await message.answer('Выберите продукт для покупки:', reply_markup=kb_menu)


@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()


@dp.message_handler(text=['Рассчитать'])
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb_in)


@dp.message_handler(text=['Информация'])
async def main_menu(message):
    await message.answer('Предлагаем выполнить расчет калорий (в день) для правильного подбора продуктов:')


@dp.callback_query_handler(text="formulas")
async def get_formulas(call):
    await call.message.answer("Формула расчета для женщин: \n"
                              "(10 × вес в килограммах) + (6,25 × рост в сантиметрах) \n− (5 × возраст в годах) − 161")
    await call.answer()


@dp.callback_query_handler(text="calories")
async def set_age(call):
    await call.message.answer("Введите свой возраст:")
    await UserState.age.set()
    await call.answer()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()

    # await message.answer(f' age: {data["age"]}, growth: {data["growth"]}, weight: {data["weight"]}')
    norm = 10.0 * float(data["weight"]) + 6.25 * float(data["growth"]) - 5.0 * float(data["age"]) - 161.0
    await message.answer(f'Ваша норма калорий: {norm}', reply_markup=kb)

    await state.finish()


@dp.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
