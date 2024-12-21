import asyncio
import logging
from aiogram import (Bot, Dispatcher)
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove)
import time
import requests
from aiogram.utils.markdown import hlink
from aiogram.fsm.state import StatesGroup, State


rply = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Обувь"),
                    KeyboardButton(text="Верхняя одежда"),
                ],
                [
                    KeyboardButton(text='Штаны/брюки'),
                    KeyboardButton(text='Другое')
                ]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )

nezakaz = ReplyKeyboardRemove()


class Application(StatesGroup):
    name = State()
    name_2 = State()
    name_3 = State()
    description = State()
    description_2 = State()


dp = Dispatcher(storage=MemoryStorage())


TOKEN = 'HG7yXuo'


data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
CNY = data['Valute']['CNY']['Value']
CNY_2 = CNY + 1
USD = data['Valute']['USD']['Value']
USD_2 = USD + 1
EUR = data['Valute']['EUR']['Value']
EUR_2 = EUR + 1

text_link = hlink('группе ВК','https://vk.com/batbuyers')


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f" 📦 Привет, {message.from_user.first_name}! \nЯ Bat_buyers_bot 🦇. С помощью меня ты можешь узнать актуальный курс на валюты, посчитать стоимость вещи с доставкой до твоего города и д.р.\nНастоятельно рекомендую ознакомиться с правилами пользования бота.")
    time.sleep(3)
    await message.answer_sticker('CAACAgIAAxkBAAEL0KRmB9po--fhBRZpslDeQ3T96N_LYwACBBMAAowt_QeyDcpuxYwKMzQE')
    time.sleep(2)
    await message.answer('С помощью меня, Вы можете \n1.Рассчитать сумму Вашего заказа \n2.Узнать актуальный курс Валют \n3.Заказать одежду/обувь.')


@dp.message(Command('rules'))
async def rules(msg: Message):
    await msg.answer("Правила читать здесь: \nhttps://telegra.ph/Pravila-ispolzovaniya-bota-04-08")


@dp.message(Command("currency"))
async def helpy(message: Message) -> None:
    await message.answer(f'Текущий курс: \n 🇨🇳 1 CNY = {round(CNY ,2)} \n 🇺🇸 1 USD = {round(USD, 2)} \n 🇪🇺 1  EUR = {round(EUR, 2)}')


@dp.message(Command('calc'))
async def calcu(msg: Message, state: FSMContext):
    await msg.answer('Напишите сумму в 🇨🇳Юанях и я посчитаю всю сумму с доставкой до Вашего города!')
    await state.set_state(Application.name)


@dp.message(Application.name)
async def get_name(message: Message, state: FSMContext):
        await state.update_data(name=message.text)
        await state.set_state(Application.name)
        result = int(message.text) * CNY_2 + 1500
        result_2 = round(result, 1)
        carz_3 = await message.reply(f'Стоимость заказа составляет: ' + str(result_2) + '\nЕсли готовы сделать заказ, нажмите /buy и следуйте инструкции.')
        await carz_3.forward(chat_id=-1002138817907)
        await state.clear()


@dp.message(Command('calcusd'))
async def calcu(msg: Message, state: FSMContext):
    await msg.answer('Напишите сумму в 🇺🇸Долларах и я посчитаю всю сумму с доставкой до Вашего города!')
    await state.set_state(Application.name_2)


@dp.message(Application.name_2)
async def get_name(message: Message, state: FSMContext):
        await state.update_data(name=message.text)
        await state.set_state(Application.name_2)
        resulty = int(message.text) * USD_2 + 1500
        result_3 = round(resulty, 1)
        carz_2 = await message.reply(f'Стоимость заказа составляет: ' + str(result_3) + '\nЕсли готовы сделать заказ, нажмите /buy и следуйте инструкции.')
        await carz_2.forward(chat_id=-1002138817907)
        await state.clear()


@dp.message(Command('calceur'))
async def calcu(msg: Message, state: FSMContext):
        await msg.answer('Напишите сумму в 🇪🇺Евро и я посчитаю всю сумму с доставкой до Вашего города!', reply_markup=nezakaz)
        await state.set_state(Application.name_3)


@dp.message(Application.name_3)
async def get_name(message: Message, state: FSMContext):
        await state.update_data(name=message.text)
        await state.set_state(Application.name_3)
        resulta = int(message.text) * EUR_2 + 1500
        result_4 = round(resulta, 1)
        carz = await message.reply(f'Стоимость заказа составляет: ' + str(result_4) + '\nЕсли готовы сделать заказ, нажмите /buy и следуйте инструкции.')
        await carz.forward(chat_id=-1002138817907)
        await state.clear()


@dp.message(Command('buy'))
async def get_name(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await msg.answer(text="Отправьте контактные данные, и в скорем мы свяжемся с Вами.")
    await msg.answer(f"Один штрих, дайте Ваши контактные данные(@...), или номер телефона, для того чтобы Наш представитель мог с Вами связаться.\n\nТакже! Можете ознакомиться с полным ассортиментом в нашей {text_link}.", reply_markup=nezakaz)
    await state.set_state(Application.description)


@dp.message(Application.description)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await message.answer(
    f"Принято!\nЧто Вы желаете заказать?", reply_markup=rply)
    await message.forward(chat_id=-1002138817907)
    await state.set_state(Application.description_2)


@dp.message(Application.description_2)
async def process_name_2(message: Message, state: FSMContext) -> None:
    await state.set_state(Application.description_2)
    await message.forward(chat_id=-1002138817907)
    await message.answer('Принято, скоро с Вами свяжется наш представитель по поводу Вашего заказа.')
    await message.answer_sticker('CAACAgIAAxkBAAEL3o5mE-XFmxvzROK3-L10VPWusqkX8QACBxMAAowt_QeCozYtb0HPuzQE')
    await state.clear()


@dp.message()
async def privet(msg:Message) -> None:
    await msg.answer('Привет, это сообщение от создателя. Мне кажется ты ввел не ту команду...\nТакже, если что-то не работает, напиши создателю бота :)')


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)
if __name__ == "__main__":
    logging.basicConfig()
    asyncio.run(main())
