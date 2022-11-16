from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import translators as ts
import asyncio
import aioschedule
import func
import dbutil
from ttm import Text_to_Music
from config import bot_api_key
from config import email_from_api

bot = Bot(token=bot_api_key)
dp = Dispatcher(bot)
ttm = Text_to_Music(email_from_api)


@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    if not message.from_user.is_bot:
        user = [message.from_user.id, message.from_user.first_name, message.from_user.last_name,
                message.from_user.username, message.from_user.language_code]
        func.createuser(user)
        await message.answer(
            "Данный бот создан для тестирования MubertAI. Пришлите мне сообщение и я вместе MubertAI создам музыку под данную тему сообщения.")
        await message.delete()
        return


@dp.message_handler()
async def echo_send(message: types.Message):
    if not message.from_user.is_bot:
        user = [message.from_user.id, message.from_user.first_name, message.from_user.last_name,
                message.from_user.username, message.from_user.language_code]
        state = func.checkstate(user)
        if state == 0:
            answ = ts.google(message.text, to_language='en')
            await message.delete()
            text = "В течении 1-5минут бот сгенерирует и отправит вам Ваш музончик :)"
            await bot.send_message(message.from_id, text)
            music = await ttm.generate_track_by_prompt(answ)
            await bot.send_audio(chat_id=message.from_id, audio=music)
            return


async def setup_bot_commands():
    bot_commands = [
        types.BotCommand(command="/start", description="Для сброса и возвращения в главное меню"),
    ]
    await bot.set_my_commands(bot_commands)


async def scheduler():
    aioschedule.every(1).minutes.do(send)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(_):
    dbutil.checkandupdatedb()
    await setup_bot_commands()
    asyncio.create_task(scheduler())


async def send():
    # await bot_message.reminders(bot)
    return


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
