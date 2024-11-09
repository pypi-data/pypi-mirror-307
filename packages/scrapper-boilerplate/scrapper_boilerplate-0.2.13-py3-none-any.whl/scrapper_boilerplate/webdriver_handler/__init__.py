import logging
import random

from time import sleep

from scrapper_boilerplate.setup import setSeleniumWith
from scrapper_boilerplate.parser_handler import init_parser

from selenium.webdriver.chrome import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException


def scrolldown(driver, element=None):
    """
    Scroll down the page
    args:
        - driver: Selenium Webdriver
    return: void
    """

    SCROLL_PAUSE_TIME = 0.5

    # Get scroll height
    if element:
        last_height = driver.execute_script("return arguments[0].scrollHeight", element)

    else:
        last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        if element:
            driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", element)

        else: 
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page and increments one more second
        SCROLL_PAUSE_TIME += 1
        sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        if element:
            new_height = driver.execute_script("return arguments[0].scrollHeight", element)
        
        else:
            new_height = driver.execute_script("return document.body.scrollHeight")


        if new_height == last_height:
            break
        last_height = new_height


def smooth_scroll(driver, element=None):
    """
    Smooth scroll the page
    args:
        - driver: Selenium Webdriver
    returns:
        - void
    """

    scroll = .1
    while scroll < 9.9:
        if not element:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight/%s);" % scroll)
        
        else:
            driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight/%s);" % (element, scroll))
        scroll += .01


def load_dynamic_page(url, headless=True, remote=True, scroll=False,**kwargs):
    """
    Load a dynamic page
    args:
        - url: str, the url of the page you want to load
        - headless: bool, True if you want to run the browser in headless mode
    returns:
        - driver: Selenium Webdriver
    """

    with setSeleniumWith(
        headless=headless, 
        remote_webdriver=remote, 
        profile=kwargs.get("profile"), 
        profile_name=kwargs.get("profile_name")
    ) as driver:
        driver.get(url)
        driver.implicitly_wait(220)
        
        if scroll:
            scrolldown(driver)

        if kwargs.get("screenshot"):
            driver.save_screenshot(kwargs.get("screenshot_name"))
            
        html = driver.find_element(By.TAG_NAME, 'html')
        return init_parser(html.get_attribute('outerHTML'))


def load_code(driver, full_page=False):
    """
    Load code from a page

    args:
        - driver: Selenium Webdriver
    
    returns:
        - code: Beautifulsoap Obj, the code from the page
    """
    if full_page:
        code = driver.page_source
        return init_parser(code)

    code = driver.get_attribute('outerHTML')
    return init_parser(code)


def explicit_wait(driver:webdriver, tag:By, element:str, timeout:int=10, screenshot:bool=False, screenshot_name:str="screenshot.png", raise_error:bool=False) -> webdriver:
    """explicitly wait for an element to load

    Args:
        driver (webdriver): selenium webdriver instance
        tag (_type_): the tag instance
        element (str): the selector of the element
        timeout (int, optional): the limit of wait to load element. Defaults to 10.
        screenshot (bool, optional): if enable screenshot on error. Defaults to False.
        screenshot_name (str, optional): name of screenshot. Defaults to "screenshot.png".
        raise_error (bool, optional): if raises timeout error or return. Defaults to False.

    Raises:
        TimeoutException: _description_

    Returns:
        webdriver: _description_
    """

    try:
        handler = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((tag, element))
        )
        return handler
    
    except TimeoutException:
        if screenshot:
            driver.save_screenshot(screenshot_name)
        logging.error("error to explicitly wait")
        
        if raise_error: 
            raise TimeoutException 
        
        return


def mimic_user_input(webElement:webdriver, text:str):
    """mimic user input, write in input field letter by letter

    Args:
        webElement (webdriver): the webdriver instance
        text (str): input text
    """
    for char in text:
        sleep(random.uniform(0.1, 0.2))
        webElement.send_keys(char)
