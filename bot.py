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
import psutil
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

@dispatcher.message(Command('set_pass'))
async def set_pass(messages: Message, command: CommandObject):
    reload_dotenv()
    data = command.args
    dotenv.set_key(dotenv_path, "P2PSECRET", data)

    print(os.getenv('P2PSECRET'))
    await bot.send_message(chat_id=chat_id, text=f"Установлен временный пароль: {data}")

@dispatcher.message(Command('set_username'))
async def set_username(messages: Message, command: CommandObject):

    data = command.args
    dotenv.set_key(dotenv_path, "P2PUSER", data)
    reload_dotenv()
    print(os.getenv('P2PUSER'))

    await bot.send_message(chat_id=chat_id, text=f"Установлен логин для входа: {data}")

@dispatcher.message(Command('set_user_password'))
async def set_user_password(messages: Message, command: CommandObject):

    data = command.args
    dotenv.set_key(dotenv_path, "P2PPASS", data)
    reload_dotenv()
    print(os.getenv('P2PPASS'))
    await bot.send_message(chat_id=chat_id, text=f"Установлен пароль для входа: {data}")

@dispatcher.message(Command('get_last_course'))
async def get_last_course(messages: Message, command: CommandObject):
    reload_dotenv()

    try:
        data = os.getenv('LAST_COURSE')
        user_course = os.getenv('USER_COURSE')
        percent = 100 - (float(user_course) / float(data)) * 100
        await bot.send_message(chat_id=chat_id, text=f"Последнее значение курса из ЛК: {data}, отклонение: {percent:.3f} %")
    except:
        await bot.send_message(chat_id=chat_id, text=f"Не найдено последнее значение курса из ЛК.")

@dispatcher.message(Command('get_c'))
async def get_с(messages: Message, command: CommandObject):
    reload_dotenv()
    try:
        data = os.getenv('USER_COURSE')
        await bot.send_message(chat_id=chat_id, text=f"Последнее установленное эталонное значение курса: {data}")
    except:
        await bot.send_message(chat_id=chat_id, text=f"Не найдено последнее значение эталонного курса.")

@dispatcher.message(Command('get_d'))
async def get_d(messages: Message, command: CommandObject):
    reload_dotenv()
    try:
        data = os.getenv('DEVIATION')
        await bot.send_message(chat_id=chat_id, text=f"Последний установленный процент отклонения курса: {data} %")
    except:
        await bot.send_message(chat_id=chat_id, text=f"Не найдено последнее значение процента отклонения.")

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
               f" Перед запуском парсера: \n"
               f" /set_username - установить логин для парсера.\n"
               f" /set_user_password - установить пароль пользователя для парсера. \n"
               f" /set_pass - установить временный пароль. \n"                          
               f" /start_parser - удаленный запуск парсера из бота. \n"
               f" /get_last_course - Вывести последнее значение полученное из ЛК. \n"
               f" /get_c - Вывести последнее эталонного курса'. \n"
               f" /get_d - Вывести последнее значение процента отклонения. \n"

               )

    await bot.send_message(chat_id=chat_id, text=f"{message}")



async def job():
    reload_dotenv()
    user_course = os.getenv('USER_COURSE')
    if os.path.exists(data_path):
        print("Файл выгрузки найден")
        reload_dotenv()
        with open(data_path, 'r', encoding='utf-8') as f:
            data = f.read()
            f.close()
        parsed_course = float(data)
        old_parsed_course = parsed_course
        os.environ["LAST_COURSE"] = str(old_parsed_course)
        percent = 100 - (float(user_course) / parsed_course) * 100
        print('Первый запуск, нет файла выгрузки')

        os.remove(data_path)
        try:
            course_history.append(parsed_course)
        except:
            print("Первая выгрузка")

        devation = float(os.getenv('DEVIATION')) - float(os.getenv('DEVIATION')) * 2

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
                             f"Эталонное значение: {user_course}\n"
                             f"Текущий заданный  процент падения: {devation}\n"
                             f"Курс от эталонного значения уменьшился на: {percent:.3f} %\n"
                             f"Последнее значение из личного кабинета: {parsed_course}")
                    # print(messg)
                    await bot.send_message(chat_id=chat_id, text=f"{messg}")
    else:
        print("Нет файла выгрузки")



# async def cloudflare_job():
#     reload_dotenv()
#     cloudflare = os.getenv('CLOUDFLARE')
#     if cloudflare == '1':
#         reload_dotenv()
#         dotenv.set_key(dotenv_path, 'CLOUDFLARE', '0')
#         await bot.send_message(chat_id=chat_id,
#                               text=f'Найден cloudflare. Необходимо в браузере бота пройти проверку и перезапустить Run.exe Работа бота завершена')
#         print('cloudflare_job отработал')
#         PROCNAME = "python.exe"
#
#         for proc in psutil.process_iter():
#             if proc.name() == PROCNAME:
#                 proc.kill()
#
#
#     else:
#         print("Задание отработало, clodflare не найден.")



async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(job, 'interval', seconds=10)
    # scheduler.add_job(cloudflare_job, 'interval', seconds=10)
    scheduler.start()
    exec_path = sys.executable
    subprocess.Popen([exec_path, 'main.py'])
    reload_dotenv()
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
    reload_dotenv()
    run()