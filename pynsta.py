from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
import random

from secrets import username, password

class instaBot():
    narrow = True
    wide = True

    def __init__(self):
        # r before string means that it is read as raw
        self.driver = webdriver.Chrome(executable_path=r"C:\Program Files (x86)\Google\Driver\chromedriver.exe")

    def login(self):
        # navigate to webpage
        self.driver.get('https://instagram.com')
        time.sleep(2)

        # click link to login to existing account
        login_lnk = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[2]/p/a')
        login_lnk.click()
        time.sleep(4)
    
        # input for Username / e-mail / phone number
        cred_in = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input')
        cred_in.send_keys(username)

        # input for password
        pwd_in = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input')
        pwd_in.send_keys(password)

        # click button to log in to your account
        login_btn = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button/div')
        login_btn.click()
        time.sleep(5)

    def notificationsPopUp(self):
        noNotifications_btn = self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/button[2]')
        noNotifications_btn.click()
        time.sleep(0.4)

    # define argument for wide or 
    def wideOrNarrow(self):
        try:
            self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/section/div[1]/div[1]/div/article[1]/div[2]/section[1]/span[1]/button')
        except:
            print('Exception occured - not wide')
            wide = False

            try:
                self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/section/div[2]/div[1]/div/article[1]/div[2]/section[1]/span[1]/button')
            except:
                print('Exception occured - not narrow')
                narrow = False
            else:
                narrow = True
        else:
            wide = True
            narrow = False

        s1 = '//*[@id="react-root"]/section/main/section/div['
        s2 = ']'

        if wide is True:
            return s1 + str(1) + s2            
        elif wide is False:
            if narrow is True:
                return s1 + str(2) + s2
            elif narrow is False:
                raise Exception('Unknown error')

    def currentElement(self, subXpath, i):
        s1 = subXpath + '/div[1]/div/article['
        s2 = ']/div[2]/section[1]/span[1]/button'

        return s1 + str(i) + s2

    def search(self):
        search_textBox = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input') 
        search_textBox.send_keys(self.selectRandomTopic())
        # wait for list to appear
        time.sleep(2)

        list_element = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[2]/div[2]/div/a[1]') 
        list_element.click()
        # wait for loading page with photos
        time.sleep(5)

        firstPhoto_btn = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a')
        firstPhoto_btn.click()
        # wait for loading photo
        time.sleep(2)

    # as on first photo there is only next button, there is difference 
    # between xpath on first and following photos
    def goToSecond(self):
        next_btn = self.driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div/a')
        next_btn.click()
        time.sleep(2)
    
    def goToNext(self):
        next_btn = self.driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div/a[2]')
        next_btn.click()
        time.sleep(2)

    def like(self):
        like_btn = self.driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[2]/section[1]/span[1]/button')
        like_btn.click()


    def selectRandomTopic(self):
        tl = [line.rstrip('\n') for line in open('topics.txt')]
        c = random.choice(tl)

        return c

# TODO:
# - counter of likes given
# - sleep
# - list backup

def main():
    bot = instaBot()
    bot.login()
    bot.notificationsPopUp()

    while True:
        bot.search()
        bot.like()
        bot.goToSecond()

        while True:
            try:
                bot.like()
                bot.goToNext()
            except:
                break


if __name__ == '__main__':
    main()