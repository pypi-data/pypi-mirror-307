import os
import logging

from selenium import webdriver
from dotenv import load_dotenv
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.service import Service

load_dotenv()


def choose_driver(driver_name:str):
    if driver_name == "chrome":
        return ChromeDriverManager().install()
    elif driver_name == "firefox":
        return GeckoDriverManager().install()
    elif driver_name == "edge":
        return EdgeChromiumDriverManager().install()
    else:
        return ChromeDriverManager().install()


def setSelenium(headless=True, remote_webdriver=True, driver_name="chrome", profile=False, profile_name="default"):
    chrome_options = webdriver.ChromeOptions()
    if headless:
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('log-level=3')

    if profile:
        dir_path = os.getcwd()
        profile = os.path.join(dir_path, f"{profile_name}", "profile", "wpp")
        chrome_options.add_argument(f'user-data-dir={profile}')

    if remote_webdriver:
        path = choose_driver(driver_name)
    else:
        path = os.getenv('CHROMEDRIVER_PATH') 

    driver = webdriver.Chrome(service=Service(executable_path=path), options=chrome_options)
    logging.info("WebDriver initialized successfully.")
    return driver


class setSeleniumWith():
    """
    Set Selenium Webdriver
    args: 
        - headless: bool, True if you want to run the browser in headless mode
        - rotate_useragent: bool, True if you want to rotate the useragent
        - remote_webdriver: bool, True if you want to download and use the remote webdriver
        - driver_name: str, the name of the driver you want to use
        - profile_name: str, the name of the profile
        - profile:bool, True if you want to use profiles

    returns:
        - webdriver: Selenium Webdriver instance
    """

    def __init__(self, headless=True, rotate_useragent=False, remote_webdriver=True, driver_name="chrome", profile=False, profile_name="default"):
        self.headless = headless
        self.rotate_useragent = rotate_useragent
        self.remote_webdriver = remote_webdriver
        self.driver_name = driver_name
        self.profile = profile
        self.profile_name = profile_name
        self.driver = None

    def __enter__(self):
        chrome_options = webdriver.ChromeOptions()
        if self.headless:
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('log-level=3')

        if self.profile:
            dir_path = os.getcwd()
            profile = os.path.join(dir_path, f"{self.profile_name}", "profile", "wpp")
            chrome_options.add_argument(f'user-data-dir={profile}')

        if self.remote_webdriver:
            path = choose_driver(self.driver_name)
        else:
            path = path = os.getenv('CHROMEDRIVER_PATH')

        self.driver = webdriver.Chrome(service=Service(executable_path=path), options=chrome_options)
        logging.info("WebDriver initialized successfully.")
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if self.driver:
                self.driver.close()
                self.driver.quit()
                logging.info("WebDriver quit successfully.")
        except Exception as e:
            logging.error(f"Error quitting WebDriver: {e}")


def init_log(filesave:bool=False, filename:str="debug.log", level=logging.INFO, **kwargs) -> None:
    
    """setup a configured custom log handler

    parameters:
        - filename (str): log filename
        - filesave (bool): if save to file or not (default:False)
        - level (logging): log leve (default:logging.INFO)

    returns:
        None
    """

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
     
    # create console handler and set level to info
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt='%d/%m/%Y %H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    if kwargs.get("error_sep") and filesave:
        # create error file handler and set level to error
        handler = logging.FileHandler(os.path.join("error.log"),"w", encoding=None, delay="true")
        handler.setLevel(logging.ERROR)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt='%d/%m/%Y %H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
   
    if filesave:
        # create debug file handler and set level to debug
        handler = logging.FileHandler(os.path.join(filename),"w")
        handler.setLevel(level)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt='%d/%m/%Y %H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
