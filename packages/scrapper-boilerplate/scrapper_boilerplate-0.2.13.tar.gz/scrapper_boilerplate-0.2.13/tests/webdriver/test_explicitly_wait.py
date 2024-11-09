from scrapper_boilerplate import explicit_wait, setSeleniumWith
from selenium.webdriver.common.by import By


def test_explicitly_wait():
    with setSeleniumWith(headless=False) as driver:
        driver.get("https://stackoverflow.com/")
        code = explicit_wait(driver, By.CSS_SELECTOR, 'h1', timeout=60)
        print(code.text)
        assert code


def test_explicitly_wait():
    with setSeleniumWith(headless=True) as driver:
        driver.get("https://stackoverflow.com/")
        code = explicit_wait(driver, By.CSS_SELECTOR, 'h1', timeout=60)
        print(code.text)
        assert code
