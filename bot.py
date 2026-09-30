import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from ai_chat import chat

# ИСПРАВЛЕНО: добавлен import os
TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_modes: dict[int, str] = {}

def get_main_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="ИИ ЧАТ"))
    builder.add(types.KeyboardButton(text="Саломалейкум"))
    return builder.as_markup(resize_keyboard=True)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Салом! Тугмаи поёнро зер кунед:", reply_markup=get_main_keyboard())

@dp.message(lambda message: message.text == "ИИ ЧАТ")
async def say_hello(message: types.Message):
    user_modes[message.from_user.id] = 'chat'
    await message.answer("Режими ИИ фаъол аст. Саволатонро нависед")

@dp.message(lambda message: message.text == "Саломалейкум")
async def say_hello_2(message: types.Message):
    await message.answer('Воалейкум АКА созаки хубаки?')

@dp.message()
async def ai_response(message: types.Message):
    # ИСПРАВЛЕНО: используем .get(), чтобы бот не падал, если кнопка не нажата
    mode = user_modes.get(message.from_user.id)
    
    if mode == 'chat':
        await message.answer('Фикр карда истодаам...')
        try:
            answer = chat(message.from_user.id, message.text)
            await message.answer(answer)
        except Exception as e:
            await message.answer(f"Хатои техникӣ: {e}")
    else:
        # Если пользователь пишет без выбора режима, просим нажать кнопку
        await message.answer("Лутфан, аввал тугмаи 'ИИ ЧАТ'-ро зер кунед.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())