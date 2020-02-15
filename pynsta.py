from selenium import webdriver
import time

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
        time.sleep(3)

        # click link to login to existing account
        login_lnk = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[2]/p/a')
        login_lnk.click()
        time.sleep(3)
    
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

    # define argument for wide or 
    def wideOrNarrow(self):
        # TODO: go to next element. Identify element as clicked.
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

        # TODO improve logic
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
        
    # TODO make it like
    def like(self, subXpath, i):
        curElmn = self.currentElement(subXpath, i)
        like_btn = self.driver.find_element_by_xpath(curElmn)
        like_btn.click() 

bot = instaBot()
bot.login()
bot.notificationsPopUp()

subXpath = bot.wideOrNarrow()

for i in range(1,5):
    bot.like(subXpath, i)
    time.sleep(1)