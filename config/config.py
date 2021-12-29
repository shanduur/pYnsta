import os
import random
import re
from pathlib import Path
import jstyleson as json

from logger import log


data = dict()
if os.path.isfile('./.pynsta.json'):
    with open('./.pynsta.json') as json_file:
        data = json.load(json_file)
elif os.path.isfile(os.path.join(Path.home(), './.pynsta.json')):
    with open('./.pynsta.json') as json_file:
        data = json.load(json_file)


def parse_time(t: str) -> float:
    multiplier = {
        "h": 3600,
        "m": 60,
        "s": 1,
    }[t[-1].lower()]
    
    return float(t[:-1]) * multiplier


class Config():
    def __init__(self) -> None:
        t = os.getenv('SLEEP_TIME')
        if not t:
            try:
                t = data["config"]["wait-time"]
            except KeyError:
                log.error("sleep time not set, falling back to default", extra={"wait-time": "60s"})
                t = "60s"

        try:
            self.wait_time = parse_time(t)
        except ValueError:
            log.error("unable to parse wait time, falling back to default", extra={"wait-time": "60s"})
            self.wait_time = 60.0

        max_likes = os.getenv('MAX_LIKES')
        if not max_likes:
            try:
                max_likes = data["config"]["max-likes"]
            except KeyError:
                log.error("max-likes count not set, falling back to default", extra={"max-likes": "1000"})
                max_likes = 1000
        self.max_likes = int(max_likes)


class Instagram():
    def __init__(self) -> None:
        self.login = os.getenv('INSTA_LOGIN')
        if not self.login:
            try:
                self.login = data["instagram"]["login"]
            except KeyError:
                raise KeyError("no login set")

        self.password = os.getenv('INSTA_PASS')
        if not self.password:
            try:
                self.password = data["instagram"]["password"]
            except KeyError:
                raise KeyError("no password set")


class Selenium():
    def __init__(self) -> None:
        self.port = os.getenv('SELENIUM_PORT')
        if not self.port:
            try:
                self.port = data["selenium"]["port"]
            except KeyError:
                self.port = 4444

        self.host = os.getenv('SELENIUM_HOST')
        if not self.host:
            try:
                self.host = data["selenium"]["host"]
            except KeyError:
                self.host = 'localhost'


class Tags():
    def __init__(self) -> None:
        tags = os.getenv('HASHTAGS')
        if tags:
            tags = tags.split(',')
        else:
            try:
                tags = data["hashtags"]
            except KeyError:
                tags = ["#instagram"]

        # remove spaces, newlines and whitespace characters
        tags = [re.sub(r'/s', '', t) for t in tags]

        # check if contains hash
        tags = [t if t.startswith('#') else '#'+t for t in tags]

        # check if hashtags are valid
        tags = [t for t in tags if not t[1].isdigit()]
        tags = [t for t in tags if len(t) >= 3]
        tags = [t for t in tags if not t[1].isdigit()]

        # remove duplicates
        self.tags = list(dict.fromkeys(tags))

        self.tags_backup = tags

    # self explanatory
    def random(self) -> str:
        try:
            tag = random.choice(self.tags)
            self.tags.remove(tag)
        except IndexError:
            self.tags = self.tags_backup
            tag = random.choice(self.tags)
        except ValueError:
            pass

        self.current_tag = tag

        return tag
