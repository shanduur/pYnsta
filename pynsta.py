from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

import time
import random

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

from secrets import username, password

class instaBot():
    narrow = True
    wide = True
    topicList = []
    backupList = []

    def __del__(self):
        self.driver.quit()

    def __init__(self):
        # r before string means that it is read as raw

        opts = webdriver.ChromeOptions()
        self.driver = webdriver.Remote(command_executor=r"http://localhost:4444", options=opts)
        self.topicList = [line.rstrip('\n') for line in open('topics.txt')]
        self.backupList = self.topicList

    def login(self):
        # navigate to webpage
        self.driver.get('https://instagram.com')
        time.sleep(2)

        # click link to login to existing account
        try:
            cookie_accept = self.driver.find_element_by_xpath('/html/body/div[4]/div/div/button[1]')
            cookie_accept.click()
            time.sleep(4)
        except Exception:
            print('cookies not found')
            pass
    
        # input for Username / e-mail / phone number
        cred_in = self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
        cred_in.send_keys(username)

        # input for password
        pwd_in = self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
        pwd_in.send_keys(password)

        # click button to log in to your account
        login_btn = self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button')
        login_btn.click()
        time.sleep(5)

    # close popup asking for notifications on desktop
    def notificationsPopUp(self):
        try:
            noNotifications_btn = self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/button[2]')
            noNotifications_btn.click()
            time.sleep(0.4)
        except Exception:
            print("no notifications btn")

    # OBSOLETE 
    # define if the site is displayed in wide or narrow mode
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

    # OBSOLETE 
    # create xpath for wide or narrow site
    def currentElement(self, subXpath, i):
        s1 = subXpath + '/div[1]/div/article['
        s2 = ']/div[2]/section[1]/span[1]/button'

        return s1 + str(i) + s2

    def search(self):
        search_textBoxBtn = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[1]')
        search_textBoxBtn.click()
        time.sleep(2)

        search_textBox = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input') 
        self.currentTopic = self.selectRandomTopic(self.topicList)
        self.topicList.remove(self.currentTopic)
        search_textBox.send_keys(self.currentTopic)
        # wait for list to appear
        time.sleep(2)

        list_element = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[3]/div/div[2]/div/div[1]/a') 
        list_element.click()
        # wait for loading page with photos
        time.sleep(5)

        firstPhoto_btn = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div/div[1]/div[1]/a')
        firstPhoto_btn.click()
        # wait for loading photo
        time.sleep(2)

    # as on first photo on the Top Posts part, there is only next button,
    # thus there is difference between xpath on first and following photos
    def goToSecond(self):
        next_btn = self.driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div/a')
        next_btn.click()
        time.sleep(2)
    
    # self explanatory
    def goToNext(self):
        next_btn = self.driver.find_element_by_xpath('/html/body/div[6]/div[1]/div/div/div[2]/button')
        next_btn.click()
        time.sleep(2)

    # self explanatory
    def like(self):
        like_btn = self.driver.find_element_by_xpath('/html/body/div[6]/div[2]/div/article/div/div[2]/div/div/div[2]/section[1]/span[1]/button')
        like_btn.click()
        time.sleep(1)

    # self explanatory
    def selectRandomTopic(self, l):
        c = random.choice(l)
        print(c)
        return c

    # self explanatory
    def closeInstaPost(self):
        close_btn = self.driver.find_element_by_xpath('/html/body/div[4]/div[3]/button')   
        close_btn.click()

    # self explanatory
    def goHome(self):
        home_btn = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[1]/a') 
        home_btn.click()

def main():
    bot = instaBot()
    print('logging in')
    bot.login()
    print('skiping pop ups')
    bot.notificationsPopUp()

    numberOfLikes = random.randrange(200,800, 1)
    #numberOfLikes = random.randrange(3,10,1) # for debug purposes
    print(f'likes to drop = {numberOfLikes}')
    numberOfLikesPerTag = int(numberOfLikes/len(bot.topicList))

    while True:
        # search for topic / hashtag
        bot.search()

        while True:
            try:
                numberOfLikes -= 1
                numberOfLikesPerTag -= 1
                bot.like()
                bot.goToNext()
                print(f'liked! likes left = {numberOfLikes}')
            except Exception as e:
                print(e)
                break

            if numberOfLikesPerTag < 1:
                print(f'out of likes per tag {bot.currentTopic}')
                break

            if numberOfLikes < 1:
                print('out of likes')
                break

        bot.closeInstaPost()
        bot.goHome()

        if numberOfLikes < 1:
            print('Entering sleep')
            #time.sleep(60) # for debug purposes
            time.sleep( 60 * 60 * 24 + 60 * random.randrange(1,10,1) * random.randrange(1,60,1) )
            bot.topicList = bot.backupList

if __name__ == '__main__':
    try:
        main()
    except:
        exit(1)