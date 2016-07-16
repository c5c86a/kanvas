from selenium import webdriver
import sys
from os.path import join, abspath, dirname
import logging
from selenium.webdriver.remote.remote_connection import LOGGER as ghostdriver_logger
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from locators import homePage
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from datetime import datetime
from time import sleep

logging.basicConfig(filename="python.log", level=logging.DEBUG)


class Browser:
    def __init__(self):
        path = abspath(join(dirname(dirname(__file__)), "phantomjs-2.1.1-64"))
        sys.path.append(path)       # phantomjs needs to be in path when running from pycharm
        cap = dict(DesiredCapabilities.PHANTOMJS)
        cap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0 ")
        service_args=["--webdriver-loglevel=DEBUG", "--cookies-file=ghostdriver.cookies"]
        ghostdriver_logger.setLevel(logging.DEBUG)

        #self.driver = webdriver.Firefox()
        self.driver = webdriver.PhantomJS(executable_path=path, desired_capabilities=cap, service_args=service_args)
        self.driver.timeout = {    # adds field to use only one of these values for a timeout
            "implicit": 10,
            "explicit": 10,
            "page_load": 30
        }
        self.driver.implicitly_wait(self.driver.timeout["implicit"])
        self.driver.set_window_size(1280, 768)
        self.driver.maximize_window()
        self.driver.set_page_load_timeout(self.driver.timeout["page_load"]) # driver.get uses this timeout when calling requests.get

    def close(self):
        self.driver.close()
        self.driver.quit()

    def shoot(self, msg, exception):
        self.driver.get_screenshot_as_file('%s.png' % datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        assert False, msg + str(exception)

    def locate(self, locator):
        """

        :param locator: key of a dictionary at module locators
        :return: http://selenium-python.readthedocs.io/api.html#selenium.webdriver.remote.webelement.WebElement
        """
        element = None
        wait = WebDriverWait(self.driver, self.driver.timeout["explicit"])
        method = locator.split(' ')[-1].lower()
        if method == 'xpath':
            wait.until(expected_conditions.presence_of_element_located((By.XPATH, homePage[locator])))
            element = self.driver.find_element_by_xpath(homePage[locator])
        elif method == 'id':
            element = wait.until(expected_conditions.presence_of_element_located((By.ID, homePage[locator])))
            #element = self.driver.find_element_by_id(homePage[locator])
        else:
            assert False, "Unknown method for locator " + str(locator)
        return element

    def load(self, url, iframe=None):
        tries = 0
        for i in range(5):
            try:
                self.driver.get(url)
            except:
                tries = i
                sleep(2)
            else:
                break
        if tries==4:
            self.shoot("Failed to load page ", e)
        if iframe:
            try:
                self.driver.switch_to.frame(self.locate(iframe))
            except Exception as e:
                self.shoot("Failed to switch to frame ", e)
        return self.driver.page_source
