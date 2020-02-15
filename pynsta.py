from selenium import webdriver
import time

from secrets import username, password

class instaBot():
    def __init__(self):
        # r before string means that it is read as raw
        self.driver = webdriver.Chrome(executable_path=r"C:\Program Files (x86)\Google\Driver\chromedriver.exe")

    def login(self):
        # navigate to webpage
        self.driver.get('https://instagram.com')
        time.sleep(3)

        # click link to login to existing account
        login_lnk = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[2]/p/a')
        login_lnk.click()

        # input for Username / e-mail / phone number
        cred_in = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input')
        cred_in.send_keys(username)

        # input for password
        pwd_in = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input')
        pwd_in.send_keys(password)

        # click button to log in to your account
        login_btn = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button/div')
        login_btn.click()
        time.sleep(3)

    def notificationsPopUp(self):
        noNotifications_btn = self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/button[2]')
        noNotifications_btn.click()

    def like(self):
        # TODO: go to next element. Identify element as clicked.
        like_btn = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/section/div[2]/div[1]/div/article[1]/div[2]/section[1]/span[1]/button')
        like_btn.click()
        like_btn = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/section/div[2]/div[1]/div/article[2]/div[2]/section[1]/span[1]/button')

bot = instaBot()
bot.login()