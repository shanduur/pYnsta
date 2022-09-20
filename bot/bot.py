from selenium import webdriver
from selenium.webdriver.common.by import By

import time
import random
from datetime import datetime as dt
import os

from logger import log
from bot.session import CorruptedSession, NoLongerValid, Session
import config


class Bot:
    def __init__(self) -> None:
        log.info("initializing bot")
        self.hashtags = config.Tags()
        self.config = config.Config()
        self.session = Session(account=config.Instagram(), selenium=config.Selenium(), initial_hashtag=self.hashtags.random())
        self.day_likes = random.randint(int(self.config.max_likes/2), self.config.max_likes)
        self.current_date = dt.today().date()

    def __call__(self) -> None:
        log.info("bot called, starting...")
        while True:
            if self.day_likes > 0:
                self.like()
                self.goto_next()
                self.day_likes -= 1
                log.info("like given", extra={"likes-remaining": self.day_likes})

            if self.day_likes <= 0 and self.current_date != dt.today().date():
                self.current_date == dt.today().date()
                self.day_likes = random.randint(int(self.config.max_likes/2), self.config.max_likes)
            elif self.day_likes <= 0 and self.current_date == dt.today().date():
                log.info("out of likes, waiting for date change", extra={"wait-time": "60m"})
                time.sleep(config.parse_time("1h"))
            elif self.day_likes > 0 and self.current_date != dt.today().date():
                self.current_date == dt.today().date()
                self.day_likes = random.randint(int(self.config.max_likes/2), self.config.max_likes)

    def __get_driver(self) -> webdriver.Remote:
        log.info("driver requested")
        try:
            return self.session(hashtag=self.hashtags.current_tag)
        except NoLongerValid:
            log.info("session expired, entering the wait period", extra={"wait-time": self.config.wait_time})
            self.session.disconnect()
            time.sleep(self.config.wait_time)

            self.session = Session(account=config.Instagram(), selenium=config.Selenium(), initial_hashtag=self.hashtags.random())
            return self.session(hashtag=self.hashtags.current_tag)
        except CorruptedSession as e:
            log.error("current session was corrupted, entering wait period and creating new session", extra={"wait-time": self.config.wait_time, "error": e})
            self.session.disconnect()
            time.sleep(self.config.wait_time)

            self.session = Session(account=config.Instagram(), selenium=config.Selenium(), initial_hashtag=self.hashtags.random())
            return self.session(hashtag=self.hashtags.current_tag)

    # self explanatory
    def like(self):
        log.info(">> like")
        try:
            like_btn = self.__get_driver().find_element(by=By.XPATH, value='//*[@aria-label="Like"]/parent::*/parent::button')
            like_btn.click()
            time.sleep(random.randint(2, 10))
        except Exception:
            pass

    # as on first photo on the Top Posts part, there is only next button,
    # thus there is difference between xpath on first and following photos
    def goto_second(self) -> None:
        log.info("going to 2nd pic")
        next_btn = self.__get_driver().find_element(by=By.XPATH, value='//*[@type="button"]//*[@aria-label="Next"]')
        next_btn.click()
        time.sleep(2)

    # self explanatory
    def goto_next(self) -> None:
        log.info("goiing to next pic")
        next_btn = self.__get_driver().find_element(by=By.XPATH, value='//*[@type="button"]//*[@aria-label="Next"]')
        next_btn.click()
        time.sleep(2)
