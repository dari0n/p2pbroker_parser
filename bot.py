import asyncio
import os
import subprocess
import sys
import dotenv
import multiprocessing, queue, time, random
from datetime import datetime
from aiogram import Bot, types
from aiogram import Dispatcher
from aiogram import Router, F
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message
from dotenv import load_dotenv
from aiogram.fsm.context import FSMContext
from os.path import join, dirname
import main as parser

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path, override=True)
router = Router()
user_course = os.getenv('USER_COURSE')
bot = Bot(token=os.getenv('TG_TOKEN'))
chat_id = os.getenv('CHAT_ID')
dispatcher = Dispatcher()
dispatcher.include_router(router)
data_path = 'data_src/parsed.txt'
course_history = [0]
dotenv.set_key(dotenv_path, "PARSER_ACTIVITY", '0')
"""
TODO: Переделать иерархию, добавить методы управления. ("БОТ Авторизуйся", "БОТ Текущий курс" и др.)
"""

def reload_dotenv():
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path, override=True)

@router.message(CommandStart())
async def start(messages: Message, state: FSMContext):
    await bot.send_message(chat_id=chat_id, text="Статус бота: работает.")
    await state.clear()


@dispatcher.message(Command('set_c'))
async def set_c(messages: Message, command: CommandObject):
    data = command.args
    dotenv.set_key(dotenv_path, "USER_COURSE", data)
    reload_dotenv()
    print(os.getenv('USER_COURSE'))
    await bot.send_message(chat_id=chat_id, text=f"Установлено эталонное значение курса: {data}")

@dispatcher.message(Command('set_d'))
async def set_d(messages: Message, command: CommandObject):
    data = command.args
    dotenv.set_key(dotenv_path, "DEVIATION", data)
    reload_dotenv()
    print(os.getenv('DEVIATION'))
    await bot.send_message(chat_id=chat_id, text=f"Установлен процент отклонения курса: {data} %")

@dispatcher.message(Command('start_parser'))
async def start_parser(messages: Message, command: CommandObject):
    #multiprocessing.Process(target=parser.run_parser()).start()
    reload_dotenv()
    exec_path = sys.executable
    parser_activity = os.getenv('PARSER_ACTIVITY')
    try:
        if int(parser_activity) == 0:
            subprocess.Popen([exec_path, 'main.py'])
            await bot.send_message(chat_id=chat_id, text=f"Парсер запущен.")
            dotenv.set_key(dotenv_path, "PARSER_ACTIVITY", '1')
        else:
            await bot.send_message(chat_id=chat_id, text=f"Парсер уже запущен!")
    except:
        await bot.send_message(chat_id=chat_id, text=f"Не удалось запустить парсер.")

@dispatcher.message(Command('help'))
async def help(messages: Message, command: CommandObject):
    message = (f" /start - проверка состояния работы бота.\n"
               f" /set_c - установка значения эталонного курса. Прм. /set_c 99.223  Запятые не использовать, разделитель \".\" \n"
               f" /set_d - установка процента отклонения курса. Прм. /set_d 0.2  Запятые не использовать, разделитель \".\" \n"
               f" /start_parser - удаленный запуск парсера из бота.  \".\" \n"
               )

    await bot.send_message(chat_id=chat_id, text=f"{message}")



async def job():
    if os.path.exists(data_path):
        print("Файл выгрузки найден")
        reload_dotenv()
        with open(data_path, 'r', encoding='utf-8') as f:
            data = f.read()
            f.close()
            parsed_course = float(data)
            percent = 100 - (float(user_course) / parsed_course) * 100
            os.remove(data_path)
            course_history.append(parsed_course)
            devation = float(os.getenv('DEVIATION')) - float(os.getenv('DEVIATION')) * 2
            print(devation)
            print(percent)
            if len(course_history) > 2:
                course_history.pop(0)
                print(course_history)
                if course_history[0] == course_history[1]:
                    print("Изменений курса не было")
                else:
                    # if percent > 0:
                        # messg = (f"\n"
                        #          f"Курс увеличился на: {percent:.3f} %\n"
                        #          f"Эталонное значение: {user_course}\n"
                        #          f"Последнее значение из личного кабинета: {parsed_course}")
                        # print(f"Процент увеличился на {percent:3f}")
                        # messg = f"Процент увеличился на {percent:3f}"
                    if percent < 0 and percent < devation:
                        print(f"Курс уменьшился на: {percent:.3f} %\n")
                        print(f"Текущий процент отклонения курса: {devation}")
                        messg = (f"\n"
                                 f"Курс уменьшился на: {percent:.3f} %\n"
                                 f"Эталонное значение: {user_course}\n"
                                 f"Текущий процент отклонения курса: {devation}\n"
                                 f"Последнее значение из личного кабинета: {parsed_course}")
                        #print(messg)
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
        reload_dotenv()
        asyncio.run(main())

    except (KeyboardInterrupt, SystemExit):
        pass

if __name__ == '__main__':
    run()

