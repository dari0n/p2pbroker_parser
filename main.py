from DrissionPage import ChromiumPage
import dotenv
from dotenv import load_dotenv
import os
from os.path import join, dirname
import time
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path, override=True)

tg_token = os.getenv('TG_TOKEN')
username = os.getenv('P2PUSER')
password = os.getenv('P2PPASS')
url = os.getenv('LOGIN_URL')
result_text = 0
driver = ChromiumPage()
driver.get(url)


def reload_dotenv():
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path, override=True)


def cloudflare_check():
    title = driver.title
    if title == 'Один момент…':
        try:
            i = driver.ele('.cf-turnstile-wrapper', timeout=5).shadow_root
            child = i.child()
            child.ele('.cb-lb-t').click()
        except:
            print('Не получилось прокликать')
    else:
        print('Не найден cloudflare')
        dotenv.set_key(dotenv_path, "CLOUDFLARE", '0')

    # p = ChromiumPage()
    # p.get(os.getenv('LOGIN_URL'))
    # i = p.get_frame('@src^https://challenges.cloudflare.com/cdn-cgi/challenge-platform')
    # if i:
    #     i('cb-lb-t').click()
    #try:
    # "//label[@class='ctp-checkbox-label']//span[@class='mark']"
    # "xpath://div/iframe"
    # driver("/xpath://div/iframe").ele("Подтвердите, что вы человек", timeout=4).click()
    #driver.get_frame('@src^https://challenges.cloudflare.com/cdn-cgi')('.mark').click()
    #driver("xpath://div/iframe").ele("Подтвердите, что вы человек", timeout=2.5).click()
    #print("Найден фрейм с проверкой от cloudflare")
    #return True

    #except:
    #print("iframe cloudflare не найден")
    #print(os.environ.get('USER_COURSE'))
    #return True


# def undetected(url):
#     driver = ChromiumPage()
#     driver.get(url)
#     return driver


def login():
    try:
        login_field = driver.ele('@placeholder:Введите логин').input(os.environ.get('P2PUSER'))
        if login_field is not None:
            reload_dotenv()
            driver.ele('@placeholder:Введите логин').input(os.environ.get('P2PUSER'))
            driver.ele('@placeholder:Введите пароль').input(os.environ.get('P2PPASS'))
            driver.ele('@placeholder:Введите одноразовый код').input(os.environ.get('P2PSECRET'))
            # Пока тестовые credentials, убрал клик по кнопке авторизации
            # driver.ele('@type:submit').click()
        else:
            print('Поля авторизации не найдены.')
    except:
        print('Поле авторизации не найдено')




def parse_course():
    load_dotenv(dotenv_path, override=True)
    if driver.eles('t:h3') is not None:
        i = 0
        for item in driver.eles('t:h3'):
            i += 1
            if i == 5:
                result_text = item.text[:-2].replace(',', '.')
        try:
            with open("data_src/parsed.txt", "w") as f:
                f.write(result_text)
                print(f"Текущий курс = {result_text} записан в файл")
                f.close()
                driver.refresh()
        except:
            print("Нет данных parse_course")
    else:
        print('Не найдена карточка для парсинга курса')


# def run_parser():
#     try:
#         """ Получаем обьект драйвера, открываем сайт"""
#         driver = undetected(os.environ.get('LOGIN_URL'))
#         """ Запускаем бота"""
#         while True:
#             """ Проверяем, есть ли iframe проверки cloudflare. Если фрейм есть, то пробуем обойти защиту, если нет, переходим к авторизации"""
#             #cloudflare_check(driver)
#             """ Если найдены поля авторизации, пробуем авторизоваться, если нет, пробуем парсить """
#             #autorization(driver)
#             parse_course(driver)
#             time.sleep(1)
#             driver.refresh()
#     except (KeyboardInterrupt, SystemExit):
#         driver.quit()

async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(cloudflare_check, 'interval', seconds=4)
    scheduler.add_job(login, 'interval', seconds=15)
    scheduler.add_job(parse_course, 'interval', seconds=28)
    scheduler.start()
    while True:
        await asyncio.sleep(1)


def run():
    while True:
        asyncio.run(main())


if __name__ == '__main__':
    #driver = undetected(os.environ.get('LOGIN_URL'))
    run()
    # try:
    #
    #     # while True:
    #     #     """ Проверяем, есть ли iframe проверки cloudflare. Если фрейм есть, то пробуем обойти защиту, если нет, переходим к авторизации"""
    #     #     # cloudflare_check(driver)
    #     #     """ Если найдены поля авторизации, пробуем авторизоваться, если нет, пробуем парсить """
    #     #     # autorization(driver)
    #     #     # parse_course(driver)
    #     #
    #     #     time.sleep(25)
    #
    # except (KeyboardInterrupt, SystemExit):
    #     print('Необходимо перезапустить бота')
