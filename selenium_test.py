from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
import time


def click_element(driver, element):
    try:

        find_element = driver.find_element(By.TAG_NAME, f"{element}")
        ActionChains(driver) \
            .click(find_element) \
            .perform()
        print('click element successfully')
        return True
    except:
        return False
        print('click element failed')


def test_selenium():
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")

    # options.add_argument("--headless")

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=options)

    stealth(driver,
            languages=["en-US", "en"],
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36',
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    #url = "https://bot.sannysoft.com/"
    url = 'https://p2pbroker.xyz/login'
    driver.get(url)
    while True:
        time.sleep(12)
        click_status = click_element(driver, 'iframe')
        if click_status:
            time.sleep(15)
        else:
            print("Больше iframe не найдено")
            exit()

    time.sleep(400)
    driver.quit()


if __name__ == '__main__':
    test_selenium()
