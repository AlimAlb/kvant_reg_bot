from gzip import READ
from aiogram import Bot, Dispatcher, executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
from aiogram.dispatcher.filters.state import State, StatesGroup
from sending_data_to_notion import createPage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from text import ABOUT, COURSES, NAME, PHONE, COURSE_CHOSE, OK, AGAIN


API_TOKEN = '5471358940:AAGXUerW1c6cwR9t9DPEOmVJBOGnTdCWUVM'
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    name = State()
    number = State()
    course = State()



@dp.message_handler(commands=['start'])
async def user_register(message):
    keyboard = ReplyKeyboardMarkup()
    button = KeyboardButton('/reg')
    keyboard.add(button)
    await message.answer(ABOUT,  parse_mode="Markdown", reply_markup=keyboard)

@dp.message_handler(commands=['reg'])
async def user_register(message):
    await message.answer(NAME, reply_markup=ReplyKeyboardRemove())
    await UserState.name.set()

  
@dp.message_handler(state=UserState.name)
async def get_name(message, state):
    await state.update_data(name=message.text)
    await message.answer(PHONE)
    await UserState.number.set() 


@dp.message_handler(state=UserState.number)
async def get_number(message, state):
    await state.update_data(number=message.text)
    rkm = ReplyKeyboardMarkup()
    for course in COURSES:
        rkm.add(KeyboardButton(COURSES[course]))
    await message.answer(COURSE_CHOSE, reply_markup=rkm)
    await UserState.course.set()



@dp.message_handler(state=UserState.course)
async def get_course(message, state):
    await state.update_data(course=message.text)
    await message.answer(OK, reply_markup=ReplyKeyboardRemove())
    keyboard = ReplyKeyboardMarkup()
    button = KeyboardButton('/reg')
    keyboard.add(button)
    await message.answer(AGAIN, reply_markup=keyboard)
    data = await state.get_data()
    print(data)
    createPage(data['name'], data['course'], data['number'])
    await state.finish()




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)