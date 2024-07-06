from DrissionPage import ChromiumPage
from dotenv import load_dotenv
import os
from os.path import join, dirname
import time

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path, override=True)

tg_token = os.getenv('TG_TOKEN')
username = os.getenv('P2PUSER')
password = os.getenv('P2PPASS')
url = os.getenv('URL')


def cloudflare_check(driver):
    try:
        driver('xpath://div/iframe').ele("Подтвердите, что вы человек", timeout=2.5).click()
        print("Найден фрейм с проверкой от cloudflare")
        return True
    except:
        print("iframe cloudflare не найден")
        print(os.environ.get('USER_COURSE'))
        return True


def undetected(url):
    driver = ChromiumPage()
    driver.get(url)
    time.sleep(3)
    return driver


def autorization(driver):
    try:
        driver.ele('@placeholder:Введите логин').input(os.environ.get('P2PUSER'))
        driver.ele('@placeholder:Введите пароль').input(os.environ.get('P2PPASS'))
        driver.ele('@placeholder:Введите одноразовый код').input(os.environ.get('P2PSECRET'))
        # Пока тестовые credentials, убрал клик по кнопке авторизации
        driver.ele('@type:submit').click()
        time.sleep(2)
    except:
        print('Поля авторизации не найдены. Пробуем парсить.')
        # return parse_course(driver)
        return True


def parse_course(driver):
    load_dotenv(dotenv_path, override=True)
    i = 0
    for item in driver.eles('t:h3'):
        i += 1
        if i == 5:
            result_text = item.text[:-2].replace(',', '.')

    with open("data_src/parsed.txt", "w") as f:
        f.write(result_text)
        print(f"Текущий курс = {result_text} записан в файл")
        f.close()


if __name__ == '__main__':
    try:
        """ Получаем обьект драйвера, открываем сайт"""
        driver = undetected(os.environ.get('LOGIN_URL'))
        """ Запускаем бота"""
        while True:
            """ Проверяем, есть ли iframe проверки cloudflare. Если фрейм есть, то пробуем обойти защиту, если нет, переходим к авторизации"""
            cloudflare_check(driver)
            """ Если найдены поля авторизации, пробуем авторизоваться, если нет, пробуем парсить """
            autorization(driver)
            parse_course(driver)
            time.sleep(1)
            driver.refresh()
    except (KeyboardInterrupt, SystemExit):
        driver.quit()


