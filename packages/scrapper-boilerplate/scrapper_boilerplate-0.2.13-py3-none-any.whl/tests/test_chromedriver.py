from scrapper_boilerplate import setSelenium


def test_setSelenium_console():
    with setSelenium(headless=False, remote_webdriver=True) as driver:
        driver.get("https://www.google.com")
        assert driver.title == "Google"

def test_setSelenium_headless():
    with setSelenium(headless=True, remote_webdriver=True) as driver:
        driver.get("https://www.google.com")
        assert driver.title == "Google"

