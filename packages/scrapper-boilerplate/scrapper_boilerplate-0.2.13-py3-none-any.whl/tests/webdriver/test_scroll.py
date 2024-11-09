import pytest
from scrapper_boilerplate import scrolldown, smooth_scroll, setSelenium
from time import sleep


@pytest.fixture(scope="module")
def driver():
    driver = setSelenium(headless=True)
    yield driver
    driver.quit()

def test_scrolldown(driver):
    driver.get("https://www.awwwards.com/sites/heleonic")
    driver.implicitly_wait(220)
    print("scrolling...")
    scrolldown(driver)
    sleep(5)

def test_smooth_scroll(driver):
    driver.get("https://www.awwwards.com/sites/heleonic")
    driver.implicitly_wait(220)
    print("smooth scrolling...")
    smooth_scroll(driver)
    sleep(5)
