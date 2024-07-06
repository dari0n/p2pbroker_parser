from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
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
     #
     # stealth(driver,
     #         languages=["en-US", "en"],
     #         user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36',
     #         vendor="Google Inc.",
     #         platform="Win32",
     #         webgl_vendor="Intel Inc.",
     #         renderer="Intel Iris OpenGL Engine",
     #         fix_hairline=True,
     #         )
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": '''
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_JSON;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Object;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Proxy;
        '''})
    #url = "https://bot.sannysoft.com/"
    #url = 'https://p2pbroker.xyz/login'
    #url = 'https://anycoindirect.eu'
    url="chrome://settings"

    driver.get(url)
    while True:
        driver.maximize_window()
        # SendKeys перестали работать, не открывают новую вкладку
        #ActionChains(driver).send_keys(Keys.COMMAND, "t").perform()
        #ActionChains(driver).send_keys(Keys.CONTROL, "t").perform()
        #ActionChains(driver).send_keys(Keys.LEFT_CONTROL, "t").perform()
        driver.switch_to.new_window('tab')
        #body = driver.find_element(By.ID, "search")
        time.sleep(2)
        ActionChains(driver).send_keys("https://google.com").perform()



        time.sleep(400)
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
