from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import time
import random
from scrapeanything.scraper.scraper import Scraper
from scrapeanything.utils.config import Config
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException        
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.remote_connection import LOGGER
import undetected_chromedriver as uc

import logging
import base64

class Selenium(Scraper):

    def __init__(self, config: Config, headless: bool=True, fullscreen: bool=False, window: dict={}, user_dir: str=None, disable_javascript: bool=False, proxy_address: str=None):
        url = config.get(section='SELENIUM', key='url')

        LOGGER.setLevel(logging.CRITICAL)
        
        options = Options()
        options.add_argument('log-level=3')
        options.add_argument('--disable-blink-features=AutomationControlled')        
        options.add_argument('--disable-gpu')
        options.add_argument('disable-infobars')
        options.add_argument('--disable-extensions')
        options.add_argument('disable-infobars')
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        ]
        options.add_argument(f"user-agent={random.choice(user_agents)}")        

        window_size = window['size'] if 'size' in window else []
        if len(window_size) == 0:
            options.add_argument('--start-maximized')
        else:
            self.driver.set_window_position(x=0, y=0)
            self.driver.set_window_size(width=window_size[0], height=window_size[1])

        if fullscreen is True:
            options.add_argument('--kiosk')

        if headless is True:
            options.add_argument('--headless')

        if proxy_address is not None:
            options.add_argument(f'--proxy-server={proxy_address}')

        if url is not None:
            self.driver = webdriver.Remote(command_executor=url, options=options)
        elif url is None:
            service = Service(ChromeDriverManager().install()) # Use webdriver_manager to automatically download and manage the correct version of chromedriver
            self.driver = webdriver.Chrome(service=service, options=options) # Initialize the WebDriver

        self.driver.execute_script('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')

        super().__init__()

    def on_wget(self, url):
        self.driver.get(url)
        return self.driver

    def on_xPath(self, path: str, element: any=None, timeout: int=99, is_error: bool=True):
        if timeout > 0:
            try:
                ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)              
                elements = WebDriverWait(driver=(self.driver if element is None else element), timeout=timeout, ignored_exceptions=ignored_exceptions).until(
                    EC.presence_of_all_elements_located((By.XPATH, path))
                )

                return elements

            except Exception as ex:
                if is_error is True:
                    raise NoSuchElementException(msg=f'Element with xpath {path} was not found')
                else:
                    return []

        return (self.driver if element is None else element).find_elements(by=By.XPATH, value=path)

    def on_exists(self, path, element, timeout=0, is_error: bool=False):
        element = self.driver if element is None else element

        if timeout > 0:
            try:
                ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)
                element = WebDriverWait(driver=element, timeout=timeout, ignored_exceptions=ignored_exceptions).until(
                    EC.presence_of_element_located((By.XPATH, path)))
                
                if isinstance(element, list):
                    return len(element) > 0
                else:
                    return element is not None

            except Exception as ex:
                if is_error is True:
                    raise NoSuchElementException(msg=f'Element with xpath {path} was not found')
                else:
                    return False
        else:
            try:
                if is_error is False:
                    return len(element.find_elements(by=By.XPATH, value=path)) > 0
                elif is_error is True and len(element.find_elements(by=By.XPATH, value=path)) == 0:
                    raise NoSuchElementException(msg=f'Element with xpath {path} was not found')

            except NoSuchElementException as ex:
                if is_error is True:
                    raise ex
                else:
                    return False

            except StaleElementReferenceException:
                raise StaleElementReferenceException()

    def on_get_text(self, element) -> str:
        return element.text

    def on_get_html(self, element):
        return element.get_attribute('innerHTML')

    def on_get_attribute(self, element, prop):
        return element.get_attribute(prop)

    def click_all(self, path: str, element: any=None, timeout=0, is_error: bool=True) -> None:
        elements = self.xPath(path=path, element=element, timeout=timeout, is_error=is_error)
        if elements is not None:

            try:
                element.click()
            except Exception as e:
                try:
                    self.driver.execute_script('arguments[0].click();', element)
                except:
                    try:
                        actions = ActionChains(self.driver)
                        actions.click(element).perform()
                    except:
                        return None

            return element
        else:
            return None

    def on_hover(self, path: str, element: any, is_error: bool=True, timeout: int=0) -> None:
        element = self.xPath(element=element, path=path, is_error=is_error, timeout=timeout)
        ActionChains(self.driver).move_to_element(element).perform()

    def on_click_and_hold(self, path: str, seconds: float, element: any=None, timeout: int=0, is_error: bool=True) -> None:
        element = self.xPath(path=path, timeout=timeout, is_error=is_error)
        action = ActionChains(self.driver)
        action.click_and_hold(element).perform()
        time.sleep(seconds) # sleep for N seconds
        action.release().perform()

    def on_click(self, path: str, element: any=None, timeout: int=0, pos: int=0, is_error: bool=True) -> any:
        if element is None and path is not None:
            element = self.xPath(path=path, element=element, timeout=timeout, pos=pos, is_error=is_error)
        
        if element is not None:
            if type(element) is list:
                if len(element) > 0:
                    element = element[pos]
                else:
                    return None
            try:
                element.click()
            except Exception as e:
                try:
                    self.driver.execute_script('arguments[0].click();', element)
                except Exception as e:
                    try:
                        actions = ActionChains(self.driver)
                        actions.click(element).perform()
                    except Exception as e:
                        return None

                return element
        else:
            return None

    def on_back(self) -> None:
        self.driver.back()

    def on_get_current_url(self) -> str:
        return self.driver.current_url

    def on_enter_text(self, path: str, text: str, clear: bool=False, element: any=None, timeout: int=0, is_error: bool=True) -> bool:
        element = self.on_xPath(path=path, element=element, timeout=timeout, is_error=is_error)

        if element is not None:
            if type(element) is list:
                element = element[0]

            if clear is True:
                element.send_keys(Keys.CONTROL + 'a')
                element.send_keys(Keys.BACKSPACE)

            element.send_keys(text)
            return True
        else:
            return False

    def on_solve_captcha(self, path: str):
        pass

    def on_login(self, username_text=None, username=None, password_text=None, password=None, is_error: bool=True) -> None:
        self.on_enter_text(username_text, username, is_error=is_error)
        self.on_enter_text(password_text, password, is_error=is_error)

        self.on_click('//button[@class="sign-in-form__submit-button"]')

    def on_search(self, path=None, text=None, timeout: int=0, is_error: bool=True) -> bool:
        self.on_enter_text(path=path, text=text, timeout=timeout, is_error=is_error)
        return self.on_enter_text(path=path, text=Keys.RETURN, timeout=timeout, is_error=is_error)

    def on_scroll_to_bottom(self):
        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

    def on_get_scroll_top(self):
        return self.driver.execute_script('return document.documentElement.scrollTop;')

    def on_get_scroll_bottom(self) -> None:
        return self.driver.execute_script('return document.body.scrollHeight')

    def on_select(self, path: str, option: str, element: any=None) -> None:
        element = WebDriverWait(self.driver if element is None else element, 10).until(
            EC.presence_of_element_located((By.XPATH, path))
        )

        if element is not None:
            Select(element).select_by_visible_text(option)

    def on_get_image_from_canvas(self, path, local_path, element) -> str:
        image_filename = f'{local_path}/image.png'

        # get the base64 representation of the canvas image (the part substring(21) is for removing the padding 'data:image/png;base64')
        base64_image = self.driver.execute_script(f"return document.querySelector('{path}').toDataURL('image/png').substring(21);")

        # decode the base64 image
        output_image = base64.b64decode(base64_image)

        # save to the output image
        with open(image_filename, 'wb') as f:
            f.write(output_image)

        return image_filename

    def on_switch_to(self, element: any) -> None:
        if element == 'default':
            self.driver.switch_to.default_content()
        else:
            self.driver.switch_to.frame(element)

    def on_screenshot(self, file: str) -> None:
        self.driver.get_screenshot_as_file(file)

    def on_freeze(self) -> None:
        self.driver.execute_cdp_cmd('Emulation.setScriptExecutionDisabled', { 'value': True })

    def on_unfreeze(self) -> None:
        self.driver.execute_cdp_cmd('Emulation.setScriptExecutionDisabled', { 'value': False })

    def on_get_cookies(self) -> 'list[dict]':
        return self.driver.get_cookies()
    
    def on_drag_and_drop(self, path_from: str, path_to: str) -> None:
        element = self.xPath(path=path_from)
        target = self.xPath(path=path_to)
        ActionChains(self.driver).drag_and_drop(element, target).perform()

    def on_close(self):
        self.driver.quit()