from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import numpy as np

class controlPanelClass(): 
    def __init__(self): 
        self.errorArrayCurrent=np.zeros(7)
        self.currentRateArray=np.zeros(7)
        self.desiredRateArray=np.zeros(7)
        self.deltaRateArray=np.zeros(7)
        self.desiredClicksArray=np.zeros(7)
        self.clicksExecuteArray=np.zeros(7)
        self.rateParamsArray=np.zeros(7)

        self.ratePerClick=0.1
        self.rotationRateParam=0.03
        self.translationRateParam=0.015
        self.rateParamsArray=[self.rotationRateParam,self.rotationRateParam,self.rotationRateParam,self.translationRateParam,self.translationRateParam,self.translationRateParam,-self.translationRateParam]

    #def reset(self):
    #    self.errorArrayCurrent=np.zeros(7)
    #    self.currentRateArray=np.zeros(7)
    #    self.desiredRateArray=np.zeros(7)
    #    self.desiredClicksArray=np.zeros(7)
    #    self.currentClicksArray=np.zeros(7).astype(int)
    #    self.clicksExecuteArray=np.zeros(7)

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
        self.currentRateArray[0]  =float(browser.find_element_by_xpath("//div[@id='roll']/div[contains(@class, 'rate')]").text[:-3])
        self.currentRateArray[1]  =float(browser.find_element_by_xpath("//div[@id='pitch']/div[contains(@class, 'rate')]").text[:-3])
        self.currentRateArray[2]  =float(browser.find_element_by_xpath("//div[@id='yaw']/div[contains(@class, 'rate')]").text[:-3])
        #Translation Rates
        self.currentRateArray[6] = float(browser.find_element_by_xpath("//div[@id='rate']/div[contains(@class, 'rate')]").text[:-4])

    def calcClicksArray(self):
        #self.desiredRateArray=np.power(self.errorArrayCurrent,2)
        self.desiredRateArray=np.multiply(self.errorArrayCurrent,self.rateParamsArray)
        self.deltaRateArray=np.subtract(self.desiredRateArray,self.currentRateArray)
        self.clicksExecuteArray=np.divide(self.deltaRateArray,self.ratePerClick)
        self.clicksExecuteArray=np.clip(self.clicksExecuteArray,-10,10)
        self.clicksExecuteArray=np.sign(self.clicksExecuteArray) * np.ceil(np.abs(self.clicksExecuteArray))      
        #self.clicksExecuteArray=np.ceil(self.clicksExecuteArray) #was around
        self.clicksExecuteArray=self.clicksExecuteArray.astype(int)
        print('calcClicksArray desided on =',self.clicksExecuteArray)
    
    def clickButtonsArray(self):
        print('clickButtonsArray received =',self.clicksExecuteArray)
        if self.clicksExecuteArray[0]>0:
            self.clickButton('roll-right-button',np.absolute(self.clicksExecuteArray[0]),timeDeltaSameClicks)
        else: 
            self.clickButton('roll-left-button',np.absolute(self.clicksExecuteArray[0]),timeDeltaSameClicks)
        if self.clicksExecuteArray[1]>0:
            self.clickButton('pitch-down-button',np.absolute(self.clicksExecuteArray[1]),timeDeltaSameClicks)
        else: 
            self.clickButton('pitch-up-button',np.absolute(self.clicksExecuteArray[1]),timeDeltaSameClicks)
        if self.clicksExecuteArray[2]>0:
            self.clickButton('yaw-right-button',np.absolute(self.clicksExecuteArray[2]),timeDeltaSameClicks)
        else: 
            self.clickButton('yaw-left-button',np.absolute(self.clicksExecuteArray[2]),timeDeltaSameClicks)
        if self.clicksExecuteArray[6]>0:
            self.clickButton('translate-backward-button',np.absolute(self.clicksExecuteArray[6]),timeDeltaSameClicks)
        else: 
            self.clickButton('translate-forward-button',np.absolute(self.clicksExecuteArray[6]),timeDeltaSameClicks)
        #self.clickButton('translate-up-button',2,timeDeltaSameClicks)
        #self.clickButton('translate-down-button',2,timeDeltaSameClicks)
        #self.clickButton('translate-right-button',2,timeDeltaSameClicks)
        #self.clickButton('translate-left-button',2,timeDeltaSameClicks)

    def clickButton(self,buttonId,timesNum,timeDeltaSameClicks):
        self.buttonElement=browser.find_element_by_id(buttonId)
        for idx in range(timesNum):
            self.buttonElement.click()
            time.sleep(timeDeltaSameClicks)


    def printInstruments(self):
        print(self.errorArrayCurrent)
        print(self.currentRateArray)
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
wait = WebDriverWait(browser, 1000)
wait.until(EC.element_to_be_clickable((By.ID, 'translate-up-button')))
time.sleep(waitAfterButtonsClickable)
print('<<<<<<<<<<<< Script is Ready! >>>>>>>>>>>>>')

#Class init
controlPanel=controlPanelClass()
#First read check
controlPanel.readInstruments()
controlPanel.printInstruments()

#TODO: current clicks is wrong (shows 3 when in fact 0)

#The loop
#while np.absolute(controlPanel.errorArrayCurrent[1]) > 0.01:
while 1:
    controlPanel.readInstruments()
    controlPanel.calcClicksArray()
    print('errorArrayCurrent=',controlPanel.errorArrayCurrent)
    print('currentClicksArray=',controlPanel.currentRateArray)
    print('desiredClicksArray=',controlPanel.desiredRateArray)
    print('clicksExecuteArray=',controlPanel.deltaRateArray)
    print('clicksExecuteArray=',controlPanel.clicksExecuteArray)
    controlPanel.clickButtonsArray()
    #time.sleep(0.5)

#reset controlPanel class
controlPanel=controlPanelClass()

#controlPanel.clickButton('roll-left-button',2,timeDeltaSameClicks)
#controlPanel.clickButton('roll-right-button',2,timeDeltaSameClicks)
#controlPanel.clickButton('pitch-up-button',2,timeDeltaSameClicks)
#controlPanel.clickButton('pitch-down-button',2,timeDeltaSameClicks)
#controlPanel.clickButton('yaw-left-button',2,timeDeltaSameClicks)
#controlPanel.clickButton('yaw-right-button',2,timeDeltaSameClicks)
#
#controlPanel.clickButton('translate-up-button',2,timeDeltaSameClicks)
#controlPanel.clickButton('translate-down-button',2,timeDeltaSameClicks)
#controlPanel.clickButton('translate-right-button',2,timeDeltaSameClicks)
#controlPanel.clickButton('translate-left-button',2,timeDeltaSameClicks)
#controlPanel.clickButton('translate-forward-button',5,timeDeltaSameClicks)
#controlPanel.clickButton('translate-backward-button',2,timeDeltaSameClicks)




#if __name__ == "__main__":
#    main()


#stuff that work but are not needed
#rollId=browser.find_elements_by_id('roll')
#rollError=rollId.find_element_by_class_name('error')


