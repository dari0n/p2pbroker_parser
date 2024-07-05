import dotenv
from DrissionPage import ChromiumPage
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


def cloudflare_check(driver, element):
    try:
        # find_element = driver.find_element(By.TAG_NAME, f"{element}")
        # ActionChains(driver) \
        #     .click(find_element) \
        #     .perform()
        # print('click element successfully')
        driver.ele(element).click()
        return True
    except:
        return False
        print('Не найден iframe cloudflare')



def undetected(url):
    driver = ChromiumPage()
    driver.get(url)
    time.sleep(8)
    # driver.close()
    autorization(driver)




def autorization(driver):
    cloudflare_check(driver,'iframe')
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