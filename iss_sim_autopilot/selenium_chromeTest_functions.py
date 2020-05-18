from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import numpy as np

class controlPanelClass(): 
    def __init__(self): 
        self.errorArray=np.zeros(7)
        self.rateArray=np.zeros(7)
        self.clicksArray=np.zeros(7)
    def clickButton(self,buttonId,timesNum,timeDeltaSameClicks):
        self.buttonElement=browser.find_element_by_id(buttonId)
        for idx in range(timesNum-1):
            self.buttonElement.click()
            time.sleep(timeDeltaSameClicks)
    def readInstruments(self):
        self.rollError = browser.find_element_by_xpath("//div[@id='roll']/div[@class='error']")
        self.pitchError = browser.find_element_by_xpath("//div[@id='pitch']/div[@class='error']")
        self.yawError = browser.find_element_by_xpath("//div[@id='yaw']/div[@class='error']")
        #Translation Error
        self.xError = browser.find_element_by_xpath("//div[@id='x-range']/div[@class='distance']")
        self.yError = browser.find_element_by_xpath("//div[@id='y-range']/div[@class='distance']")
        self.zError = browser.find_element_by_xpath("//div[@id='z-range']/div[@class='distance']")
        self.range = browser.find_element_by_xpath("//div[@id='range']/div[@class='rate']")
        #Rotation Rates
        self.rollRate = browser.find_element_by_xpath("//div[@id='roll']/div[@class='rate']")
        self.pitchRate = browser.find_element_by_xpath("//div[@id='pitch']/div[@class='rate']")
        self.yawRate = browser.find_element_by_xpath("//div[@id='yaw']/div[@class='rate']")
        #Translation Rates
        self.rangeRate = browser.find_element_by_xpath("//div[@id='rate']/div[@class='rate']")
    def printInstruments(self):
        #printing Errors
        print('rollError =',self.rollError.text)
        print('pitchError =',self.pitchError.text)
        print('yawError =',self.yawError.text)
        print('xError =',self.xError.text)
        print('yError =',self.yError.text)
        print('zError =',self.zError.text)
        print('rangeError =',self.range.text)
        #printing Rates
        print('rollRate =',self.rollRate.text)
        print('pitchError =',self.pitchRate.text)
        print('yawError =',self.yawRate.text)
        print('rangeRate =',self.rangeRate.text)

#array [roll, pitch, yaw, x, y, z, range]

#Parameters definition
timeDeltaSameClicks=0.01
waitAfterButtonsClickable=5
ratePerClick=0.1


#def main():
#chromedriver needs to be copied to disk
chromedriver = "E:\\Python\\chromedriver.exe"
browser=webdriver.Chrome(chromedriver)
#open chrome with the following address
browser.get("https://iss-sim.spacex.com/")

#wait for Begin button
wait = WebDriverWait(browser, 100)
elem = wait.until(EC.element_to_be_clickable((By.ID, 'begin-button')))
print('Click the large "Begin" button to continue!')

#wait for translate-up-button to become clickable
wait = WebDriverWait(browser, 100)
wait.until(EC.element_to_be_clickable((By.ID, 'translate-up-button')))
time.sleep(waitAfterButtonsClickable)
print('<<<<<<<<<<<< Script is Ready! >>>>>>>>>>>>>')

controlPanel=controlPanelClass()
controlPanel.readInstruments()
controlPanel.printInstruments()
#Actions
controlPanel.clickButton('roll-left-button',2,timeDeltaSameClicks)
controlPanel.clickButton('roll-right-button',2,timeDeltaSameClicks)
controlPanel.clickButton('pitch-up-button',2,timeDeltaSameClicks)
controlPanel.clickButton('pitch-down-button',2,timeDeltaSameClicks)
controlPanel.clickButton('yaw-left-button',2,timeDeltaSameClicks)
controlPanel.clickButton('yaw-right-button',2,timeDeltaSameClicks)

controlPanel.clickButton('translate-up-button',2,timeDeltaSameClicks)
controlPanel.clickButton('translate-down-button',2,timeDeltaSameClicks)
controlPanel.clickButton('translate-right-button',2,timeDeltaSameClicks)
controlPanel.clickButton('translate-left-button',2,timeDeltaSameClicks)
controlPanel.clickButton('translate-forward-button',5,timeDeltaSameClicks)
controlPanel.clickButton('translate-backward-button',2,timeDeltaSameClicks)




#if __name__ == "__main__":
#    main()


#stuff that work but are not needed
#rollId=browser.find_elements_by_id('roll')
#rollError=rollId.find_element_by_class_name('error')


