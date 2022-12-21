from aiogram import Bot, Dispatcher, executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
from aiogram.dispatcher.filters.state import State, StatesGroup
from sending_data_to_notion import createPage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from text import ABOUT, COURSES, NAME, PHONE, COURSE_CHOSE, OK, AGAIN
from utils import createcaptcha, is_name_ok, is_number_ok, is_course_ok





API_TOKEN = '5787911842:AAHu6tB6iL5RctZLSANyWocLvevavOaY6Dg'
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    captcha = State()
    name = State()
    number = State()
    course = State()
    check_data = State()
    regi = State()

@dp.message_handler(commands=['start'])
async def start(message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton('Начать регистрацию')
    keyboard.add(button)
    await message.answer(ABOUT,  parse_mode="Markdown", reply_markup=keyboard)
    await UserState.regi.set()


#Не работало тк message_handler реагирует в первую очередь на сообщение
@dp.message_handler(state=UserState.regi)
async def sendcaptcha(message,state):
    fullcaptcha = createcaptcha()
    await state.update_data(answcaptcha=fullcaptcha[1])
    await message.answer("Ваша капча:\n\n" + fullcaptcha[0] + "\n\nРешите что бы продолжить регистрацию!", reply_markup=ReplyKeyboardRemove())
    await UserState.captcha.set()


@dp.message_handler(state=UserState.captcha)
async def captch(message,state):
    data = await state.get_data()
    if message.text == str(data['answcaptcha']):
        await message.answer("Капча решена правильно!")
        await message.answer(NAME, reply_markup=ReplyKeyboardRemove())
        await UserState.name.set()

    else:
        #Не уходим из состояния пока не получим нужный ответ, капчу генерируем тут
        await message.answer("Капча решена неправильно! \n\nПопробуйте ещё раз")
        fullcaptcha = createcaptcha()
        await state.update_data(answcaptcha=fullcaptcha[1])
        await message.answer("Ваша капча:\n\n" + fullcaptcha[0] + "\n\nРешите что бы продолжить регестрацию!")
        #await UserState.regi.set()


    


@dp.message_handler(state=UserState.name)
async def get_name(message, state):
    if is_name_ok(message.text):
        await state.update_data(name=message.text)
        await state.update_data(name=message.text)
        await message.answer(PHONE)
        await UserState.number.set() 
    else:
        await message.answer('Имя не соотвествует формату :( \nПожалуйста, введите имя и фамилию с большой буквы раздельно:')
    


@dp.message_handler(state=UserState.number)
async def get_number(message, state):
    if is_number_ok(message.text):
        await state.update_data(number=message.text)
        rkm = ReplyKeyboardMarkup(resize_keyboard=True)
        for course in COURSES:
            rkm.add(KeyboardButton(COURSES[course]))
        await message.answer(COURSE_CHOSE, reply_markup=rkm)
        await UserState.check_data.set()
    else:
        await message.answer('Номер не соотвествует формату :( \nПожалуйста, введите номер без восьмерки в формате:9XXXXXXXXX:')




@dp.message_handler(state=UserState.check_data)
async def check_data(message, state):
    if is_course_ok(message.text, COURSES):
        await state.update_data(course=message.text)
        rkm = ReplyKeyboardMarkup(resize_keyboard=True)
        rkm.add(KeyboardButton('Все верно'))
        rkm.add(KeyboardButton('Хочу исправить'))
        data = await state.get_data()
        answ = f'Проверьте введенные данные🧐\n\nИмя: {data["name"]}\nНомер: +7{data["number"]}\nКурс: {data["course"]}'
        await message.answer(answ, reply_markup=rkm)
        await UserState.course.set()
    else:
        rkm = ReplyKeyboardMarkup()
        for course in COURSES:
            rkm.add(KeyboardButton(COURSES[course]))
        await message.answer('Такого курса нет в списке курсов :(\nПожалуйста, нажмите на кнопку с соотвествующим курсом.', reply_markup=rkm)
    





@dp.message_handler(state=UserState.course)
async def get_course(message, state):
    if message.text == 'Все верно':
        await message.answer(OK, reply_markup=ReplyKeyboardRemove())
        rkm = ReplyKeyboardMarkup(resize_keyboard=True)
        rkm.add(KeyboardButton('Зарегистрироваться еще раз'))
        await message.answer('Нажмите на кнопку чтобы зарегистрироваться на другой курс⬇️', reply_markup=rkm)
        data = await state.get_data()
        createPage(data['name'], data['course'], data['number'])
        await state.finish()
    elif message.text == 'Хочу исправить':
        await sendcaptcha(message,state)
    else:
        await message.answer('Пожалуйста, выберите один из двух вариантов')
        rkm = ReplyKeyboardMarkup(resize_keyboard=True)
        rkm.add(KeyboardButton('Все верно'))
        rkm.add(KeyboardButton('Хочу исправить'))

@dp.message_handler()
async def get_course(message):
    #Доделать включение заново
    if message.text == 'Зарегистрироваться еще раз':
        await start(message)




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
