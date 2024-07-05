import asyncio
import os
from datetime import datetime
from aiogram import Bot, types
from aiogram import Dispatcher
from aiogram import Router, F
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv
from aiogram.fsm.context import FSMContext
from os.path import join, dirname

dotenv_path = join(dirname(__file__), '..\\.env')
load_dotenv(dotenv_path)
router = Router()
bot = Bot(token=os.getenv('TG_TOKEN'))
chat_id = os.getenv('CHAT_ID')
dispatcher = Dispatcher()
dispatcher.include_router(router)


"""
TODO: Переделать иерархию, добавить методы управления. ("БОТ Авторизуйся", "БОТ Текущий курс" и др.)
"""

@router.message(CommandStart())
async def start(messages: Message, state: FSMContext):
    """
    Проверка статуса бота /start
    TODO: Добавить проверку статуса авторизации
    """
    await bot.send_message(chat_id=chat_id, text="Проверка ответа в чате.")
    await state.clear()


async def job():
    """
    TODO: Проверять по формуле значения курса
    Проверка отправки сообщений по расписанию.
    :return:
    """
    print('Job started')
    date = datetime.now().strftime('%d.%m.%Y')
    await bot.send_message(chat_id=chat_id, text=f"Я все еще работаю. {date}")


async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(job, 'interval', seconds=30)
    scheduler.start()
    await dispatcher.start_polling(bot)
    while True:
        await asyncio.sleep(1)


def run():
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass

