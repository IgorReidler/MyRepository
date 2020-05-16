from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import numpy as np

class controlPanelClass(): 
    def __init__(self): 
        self.errorArrayCurrent=np.zeros(7)
        self.rateArrayCurrent=np.zeros(7)
        self.rateArrayDesired=np.zeros(7)
        self.clicksArray=np.zeros(7)
        
        self.rotationRateParam=1/22.5/2
        self.translationRateParam=1/4000.0/2
        self.rateParamsArray=np.zeros(7)
        self.rateParamsArray=[self.rotationRateParam,self.rotationRateParam,self.rotationRateParam,self.translationRateParam,self.translationRateParam,self.translationRateParam,self.translationRateParam]
    def clickButtonsArray(self):
        if self.clicksArray[0]>0:
            self.clickButton('roll-left-button',np.absolute(self.clicksArray[0]),timeDeltaSameClicks)
        else: 
            self.clickButton('roll-right-button',np.absolute(self.clicksArray[0]),timeDeltaSameClicks)

        if self.clicksArray[1]>0:
            self.clickButton('pitch-up-button',np.absolute(self.clicksArray[1]),timeDeltaSameClicks)
        else: 
            self.clickButton('pitch-down-button',np.absolute(self.clicksArray[1]),timeDeltaSameClicks)

        if self.clicksArray[2]>0:
            self.clickButton('yaw-left-button',np.absolute(self.clicksArray[2]),timeDeltaSameClicks)
        else: 
            self.clickButton('yaw-right-button',np.absolute(self.clicksArray[2]),timeDeltaSameClicks)

        #self.clickButton('translate-up-button',2,timeDeltaSameClicks)
        #self.clickButton('translate-down-button',2,timeDeltaSameClicks)
        #self.clickButton('translate-right-button',2,timeDeltaSameClicks)
        #self.clickButton('translate-left-button',2,timeDeltaSameClicks)
        #self.clickButton('translate-forward-button',5,timeDeltaSameClicks)
        #self.clickButton('translate-backward-button',2,timeDeltaSameClicks)
   
    
    def clickButton(self,buttonId,timesNum,timeDeltaSameClicks):
        self.buttonElement=browser.find_element_by_id(buttonId)
        for idx in range(timesNum-1):
            self.buttonElement.click()
            time.sleep(timeDeltaSameClicks)
    def readInstruments(self):
        self.errorArrayCurrent[0] = float(browser.find_element_by_xpath("//div[@id='roll']/div[@class='error']").text[:-1])
        self.errorArrayCurrent[1]  =float(browser.find_element_by_xpath("//div[@id='pitch']/div[@class='error']").text[:-1])
        self.errorArrayCurrent[2]  =float(browser.find_element_by_xpath("//div[@id='yaw']/div[@class='error']").text[:-1])
        #Translation Error
        self.errorArrayCurrent[3]  =float(browser.find_element_by_xpath("//div[@id='x-range']/div[@class='distance']").text[:-1])
        self.errorArrayCurrent[4]  =float(browser.find_element_by_xpath("//div[@id='y-range']/div[@class='distance']").text[:-1])
        self.errorArrayCurrent[5]  =float(browser.find_element_by_xpath("//div[@id='z-range']/div[@class='distance']").text[:-1])
        self.errorArrayCurrent[6]  =float(browser.find_element_by_xpath("//div[@id='range']/div[@class='rate']").text[:-1])
        #Rotation Rates
        self.rateArrayCurrent[0]  =float(browser.find_element_by_xpath("//div[@id='roll']/div[@class='rate']").text[:-3])
        self.rateArrayCurrent[1]  =float(browser.find_element_by_xpath("//div[@id='pitch']/div[@class='rate']").text[:-3])
        self.rateArrayCurrent[2]  =float(browser.find_element_by_xpath("//div[@id='yaw']/div[@class='rate']").text[:-3])
        #Translation Rates
        self.rateArrayCurrent[6] = float(browser.find_element_by_xpath("//div[@id='rate']/div[@class='rate']").text[:-4])
    def calcClicksArray(self):
        self.clicksArray=-np.power(self.errorArrayCurrent,2)
        self.clicksArray=np.multiply(self.clicksArray,self.rateParamsArray)
        self.clicksArray=np.multiply(self.clicksArray,np.sign(self.errorArrayCurrent))
        self.clicksArray=np.floor(self.clicksArray)
        self.clicksArray=self.clicksArray.astype(int)

    def printInstruments(self):
        print(self.errorArrayCurrent)
        print(self.rateArrayCurrent)
        #printing Errors
        print('rollError =',self.errorArrayCurrent[0])
        print('pitchError =',self.errorArrayCurrent[1])
        print('yawError =',self.errorArrayCurrent[2])
        print('xError =',self.errorArrayCurrent[3])
        print('yError =',self.errorArrayCurrent[4])
        print('zError =',self.errorArrayCurrent[5])
        print('rangeError =',self.errorArrayCurrent[6])
        #printing Rates
        print('rollRate =',self.errorArrayCurrent[0])
        print('pitchRate =',self.errorArrayCurrent[1])
        print('yawError =',self.errorArrayCurrent[2])
        print('rangeRate =',self.errorArrayCurrent[6])

#array [roll, pitch, yaw, x, y, z, range]

#Parameters definition
timeDeltaSameClicks=0.01
waitAfterButtonsClickable=5

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
controlPanel.calcClicksArray()
print('clicksArray=',controlPanel.clicksArray)

#Actions
controlPanel.clickButtonsArray()

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


