import pytest
from scrapper_boilerplate import setSeleniumWith, scrolldown, smooth_scroll, sleep


@pytest.fixture(scope="module")
def driver():
    with setSeleniumWith(headless=True, remote_webdriver=True) as selenium_driver:
        yield selenium_driver

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