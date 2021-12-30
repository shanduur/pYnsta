from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

import time
import datetime as dt
import uuid

from logger import log
import config


class Session:
    def __init__(self, account: config.Instagram, selenium: config.Selenium, initial_hashtag: str = "#instagram") -> None:
        self.session_id = uuid.uuid4()
        self.login = account.login
        self.password = account.password

        opts = webdriver.ChromeOptions()
        executor = r'http://'+f"{selenium.host}:{selenium.port}"

        i = 0
        while True:
            try:
                self.valid_until = dt.datetime.now() + dt.timedelta(minutes=5)
                self.driver = webdriver.Remote(command_executor=executor, options=opts)
                break
            except Exception as e:
                log.info('waiting for connection', extra={
                    "executor": executor,
                    "valid-until": self.valid_until,
                    "error": e,
                    "repeat": i,
                })
                time.sleep(1)
            i += 1

        self.current_hashtag = initial_hashtag

        log.info("performing session startup", extra={
            "initial-hashtag": self.current_hashtag,
            "valid-until": self.valid_until,
        })

        self.__login()
        self.__close_notifications_popup()
        self.__search()

        log.info("session created successfully", extra={
            "initial-hashtag": self.current_hashtag,
            "valid-until": self.valid_until,
        })

    def __del__(self) -> None:
        log.info("deleting current session")
        try:
            self.driver.quit()
        except AttributeError as e:
            log.error("driver was not initialized", extra={"error": e})
        except WebDriverException as e:
            log.error("session was already killed", extra={"error": e})
        except Exception as e:
            log.error("ignored exception during session deletion", extra={"error": e})

    def __call__(self, hashtag: str = "#instagram") -> webdriver.Remote:
        if self.valid_until > dt.datetime.now():
            if hashtag != self.current_hashtag:
                log.info("hashtag changed", extra={"old-hashtag": self.current_hashtag, "new-hashtag": hashtag})
                try:
                    self.close_post()
                    self.go_home()
                    self.__search()
                except Exception as e:
                    raise CorruptedSession(e=e)
            return self.driver
        else:
            raise NoLongerValid(valid_until=self.valid_until)

    def __login(self) -> None:
        # navigate to webpage
        self.driver.get('https://instagram.com')
        time.sleep(2)

        # click link to login to existing account
        try:
            cookie_accept = self.driver.find_element(by=By.XPATH, value='/html/body/div[4]/div/div/button[1]')
            cookie_accept.click()
            time.sleep(4)
        except Exception:
            log.warning('cookies acceptance button not found')
            pass

        # input for Username / e-mail / phone number
        cred_in = self.driver.find_element(by=By.XPATH, value='//*[@id="loginForm"]/div/div[1]/div/label/input')
        cred_in.send_keys(self.login)

        # input for password
        pwd_in = self.driver.find_element(by=By.XPATH, value='//*[@id="loginForm"]/div/div[2]/div/label/input')
        pwd_in.send_keys(self.password)

        # click button to log in to your account
        login_btn = self.driver.find_element(by=By.XPATH, value='//*[@id="loginForm"]/div/div[3]/button')
        login_btn.click()
        time.sleep(5)

    # close popup asking for notifications on desktop
    def __close_notifications_popup(self) -> None:
        try:
            noNotifications_btn = self.driver.find_element(by=By.XPATH, value='/html/body/div[6]/div/div/div/div[3]/button[2]')
            noNotifications_btn.click()
            time.sleep(0.4)
        except Exception:
            log.info("no notifications btn")

    def __search(self) -> None:
        search_textBox = self.driver.find_element(by=By.XPATH, value='//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input') 
        search_textBox.send_keys(self.current_hashtag)
        # wait for list to appear
        time.sleep(2)

        list_element = self.driver.find_element(by=By.XPATH, value='//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[3]/div/div[2]/div/div[1]/a') 
        list_element.click()
        # wait for loading page with photos
        time.sleep(5)

        firstPhoto_btn = self.driver.find_element(by=By.XPATH, value='//*[@id="react-root"]/section/main/article/div[2]/div/div[1]/div[1]/a')
        firstPhoto_btn.click()
        # wait for loading photo
        time.sleep(2)

    def disconnect(self) -> None:
        log.info("disconnecting current session")
        try:
            self.driver.quit()
        except AttributeError as e:
            log.error("driver was not initialized", extra={"error": e})
        except WebDriverException as e:
            log.error("session was already killed", extra={"error": e})

    # self explanatory
    def close_post(self):
        close_btn = self.driver.find_element(by=By.XPATH, value='/html/body/div[6]/div[3]/button')   
        close_btn.click()
        time.sleep(2)

    # self explanatory
    def go_home(self):
        home_btn = self.driver.find_element(by=By.XPATH, value='//*[@id="react-root"]/section/nav/div[2]/div/div/div[1]/a') 
        home_btn.click()
        time.sleep(5)
        self.__close_notifications_popup()


class NoLongerValid(Exception):
    def __init__(self, valid_until: dt.datetime, message: str = "this session is no longer valid"):
        self.valid_until = valid_until
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message} (valid_until: {self.valid_until})'


class CorruptedSession(Exception):
    def __init__(self, message: str = "this session is corrupted", e: Exception = None):
        self.message = message
        self.e = e
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}: {self.e}'
