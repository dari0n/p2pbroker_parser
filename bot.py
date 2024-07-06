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

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
router = Router()
user_course = os.getenv('USER_COURSE')
bot = Bot(token=os.getenv('TG_TOKEN'))
chat_id = os.getenv('CHAT_ID')
dispatcher = Dispatcher()
dispatcher.include_router(router)
data_path = 'data_src/parsed.txt'
course_history = [0]
"""
TODO: Переделать иерархию, добавить методы управления. ("БОТ Авторизуйся", "БОТ Текущий курс" и др.)
"""


@router.message(CommandStart())
async def start(messages: Message, state: FSMContext):
    await bot.send_message(chat_id=chat_id, text="Статус бота: работает.")
    await state.clear()


async def job():
    if os.path.exists(data_path):
        print("Файл выгрузки найден")
        with open(data_path, 'r', encoding='utf-8') as f:
            data = f.read()
            f.close()
            parsed_course = float(data)
            percent = 100 - (float(user_course) / parsed_course) * 100
            os.remove(data_path)
            course_history.append(parsed_course)
            print(percent)
            if len(course_history) > 2:
                course_history.pop(0)
                print(course_history)
                if course_history[0] == course_history[1]:
                    print("Изменений курса не было")
                else:
                    if percent > 0:
                        messg = (f"\n"
                                 f"Курс увеличился на: {percent:.3f} %\n"
                                 f"Эталонное значение: {user_course}\n"
                                 f"Последнее значение из личного кабинета: {parsed_course}")
                    else:
                        messg = (f"\n"
                                 f"Курс уменьшился на: {percent:.3f} %\n"
                                 f"Эталонное значение: {user_course}\n"
                                 f"Последнее значение из личного кабинета: {parsed_course}")
                    print(messg)
                    await bot.send_message(chat_id=chat_id, text=f"{messg}")



async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(job, 'interval', seconds=10)
    scheduler.start()
    await dispatcher.start_polling(bot)
    while True:
        await asyncio.sleep(1)


def run():
    try:
        print("Бот запущен")
        asyncio.run(main())

    except (KeyboardInterrupt, SystemExit):
        pass

if __name__ == '__main__':
    run()

