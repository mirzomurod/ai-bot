import os
import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import FSInputFile
from ai_chat import chat, generate_image, search
import openai

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_modes: dict[int, str] = {}

def get_main_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="ИИ ЧАТ"))
    builder.add(types.KeyboardButton(text="🎨 РАСМ"))
    builder.add(types.KeyboardButton(text="ЧУСТУЧУ"))
    return builder.as_markup(resize_keyboard=True)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Салом! Тугмаи поёнро зер кунед:", reply_markup=get_main_keyboard())

@dp.message(lambda message: message.text == "ИИ ЧАТ")
async def say_hello(message: types.Message):
    user_modes[message.from_user.id] = 'chat'
    await message.answer("Режими ИИ фаъол аст.Саволатонро нависед")

@dp.message(lambda message: message.text == "🎨РАСМ")
async def sey_hello(message: types.Message):
     user_modes[message.from_user.id] = 'image'
     await message.answer('Чи расм тасвир кардан лозим аст? Промтро пурра нависед')

@dp.message(lambda message: message.text == "ЧУСТУЧУ")
async def say_hello(message: types.Message):
     user_modes[message.from_user.id] = 'search'
     await message.answer('Чиро чустучу кардан лозим аст? Нависед:')

@dp.message()
async def ai_response(message: types.Message):
    if user_modes[message.from_user.id] == 'chat':
         await message.answer('Фикр карда истодаам...')
         answer = chat(message.from_user.id, message.text)
         await message.answer(answer)

    elif user_modes[message.from_user.id] == 'image':
        await message.answer('🎨 Расми шумо тайёр шуда истодааст...')
        try:
           filename = generate_image(message.from_user.id, message.text)
           photo = FSInputFile(filename)
           await message.answer_photo(photo, caption="Мархамат расми шумо")
        except openai.BadRequestError:
             await message.answer('Ин расм хукуки авторирро нарушат мекунад')
    elif user_modes[message.from_user.id] == 'search':
        await message.answer('Дар чустучу...')
        result = search(message.text)
        await message.answer(result)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
        asyncio.run(main())