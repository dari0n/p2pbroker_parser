import dotenv
from DrissionPage import ChromiumPage
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os
from os.path import join, dirname
import time

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

tg_token = os.getenv('TG_TOKEN')
username = os.getenv('P2PUSER')
password = os.getenv('P2PPASS')
url = os.getenv('URL')


def cloudflare_check(driver):
    try:
        driver('xpath://div/iframe').ele("Подтвердите, что вы человек", timeout=2.5).click()
        return True
    except:
        print("iframe cloudflare не найден")
        return False




def undetected(url):
    driver = ChromiumPage()
    driver.get(url)
    time.sleep(3)
    # driver.close()
    autorization(driver)


def autorization(driver):
    cloudflare_check(driver)
    # try:
    #     driver.ele('@type:checkbox').click()
    # except:
    #     print("iframe cloudflare not found")

    driver.ele('@placeholder:Введите логин').input(os.environ.get('P2PUSER'))
    driver.ele('@placeholder:Введите пароль').input(os.environ.get('P2PPASS'))
    driver.ele('@placeholder:Введите одноразовый код').input(os.environ.get('P2PSECRET'))
    # Пока тестовые credentials, убрал клик по кнопке авторизации
    #driver.ele('@type:submit').click()
    time.sleep(2)
    print('login done')


if __name__ == '__main__':
    undetected(os.environ.get('LOGIN_URL'))
    envs = dotenv.dotenv_values()
    print(envs)

"""
username_field = soup.findAll('input', attrs = {'class' : 'mantine-TextInput-input'})
password_field = soup.findAll('input', attrs = {'class' : 'mantine-PasswordInput-root'})
onetimepass_field = soup.findAll('input', attrs = {'class' : 'mantine-TextInput-root'})
submit_button = soup.findAll('button', attrs = {'class' : 'mantine-Button-root'})  

mantine-Input-input  
"""
