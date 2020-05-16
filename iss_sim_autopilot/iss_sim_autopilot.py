import numpy as np
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class controlPanelClass(): 
    def __init__(self): 
        self.currentErrorArray=np.zeros(7)
        self.previousErrorArray=np.zeros(7)
        self.currentRateArray=np.zeros(7)
        self.desiredRateArray=np.zeros(7)
        self.deltaRateArray=np.zeros(7)
        self.desiredClicksArray=np.zeros(7)
        self.currentClicksArray=np.zeros(7)
        self.executeClicksArray=np.zeros(7)
        self.rateParamsArray=np.zeros(7)
        self.ratePerClickArray=np.zeros(7)

        self.timeDeltaErrorUpdates=0
        self.timePrevErrorUpdate=0
        self.timeCurrentErrorUpdate=0
        self.firstreadInstruments=True
        self.ratePerClickRotation=0.1
        self.ratePerClickTranslation=0.06
        #self.rateGravity=0.0065
        self.rotationRateParam=0.03
        self.translationRateParam=0.015
        self.rateParamsArray=[self.rotationRateParam,self.rotationRateParam,self.rotationRateParam,-self.translationRateParam,-self.translationRateParam,-self.translationRateParam,-self.translationRateParam]
        self.ratePerClickArray=[self.ratePerClickRotation,self.ratePerClickRotation,self.ratePerClickRotation,self.ratePerClickTranslation,self.ratePerClickTranslation,self.ratePerClickTranslation,-self.translationRateParam]
        #array [roll, pitch, yaw, x, y, z, range]

    def readInstruments(self):
        self.currentErrorArray[0] = float(browser.find_element_by_xpath("//div[@id='roll']/div[@class='error']").text[:-1])
        self.currentErrorArray[1]  =float(browser.find_element_by_xpath("//div[@id='pitch']/div[@class='error']").text[:-1])
        self.currentErrorArray[2]  =float(browser.find_element_by_xpath("//div[@id='yaw']/div[@class='error']").text[:-1])
        #Translation Error
        self.currentErrorArray[3]  =float(browser.find_element_by_xpath("//div[@id='x-range']/div[@class='distance']").text[:-1])
        self.currentErrorArray[4]  =float(browser.find_element_by_xpath("//div[@id='y-range']/div[@class='distance']").text[:-1])
        self.currentErrorArray[5]  =float(browser.find_element_by_xpath("//div[@id='z-range']/div[@class='distance']").text[:-1])
        self.currentErrorArray[6]  =float(browser.find_element_by_xpath("//div[@id='range']/div[@class='rate']").text[:-1])
        #Rotation Rates read
        self.currentRateArray[0]  =float(browser.find_element_by_xpath("//div[@id='roll']/div[contains(@class, 'rate')]").text[:-3])
        self.currentRateArray[1]  =float(browser.find_element_by_xpath("//div[@id='pitch']/div[contains(@class, 'rate')]").text[:-3])
        self.currentRateArray[2]  =float(browser.find_element_by_xpath("//div[@id='yaw']/div[contains(@class, 'rate')]").text[:-3])
        #Translation Rates read
        self.currentRateArray[6] = float(browser.find_element_by_xpath("//div[@id='rate']/div[contains(@class, 'rate')]").text[:-4])
        #Translation Rates calc

        self.currentRateArray[4] = np.multiply(self.currentClicksArray[4],self.ratePerClickTranslation)
        self.currentRateArray[5] = np.multiply(self.currentClicksArray[5],self.ratePerClickTranslation) #-0.01to account for gravity

    def calcClicksArray(self):
        #self.desiredRateArray=np.power(self.currentErrorArray,2) #for power law rate
        self.desiredRateArray=np.multiply(self.currentErrorArray,self.rateParamsArray)
        self.deltaRateArray=np.subtract(self.desiredRateArray,self.currentRateArray)
        self.executeClicksArray=np.divide(self.deltaRateArray,self.ratePerClickArray)
        self.executeClicksArray=np.clip(self.executeClicksArray,-10,10)
        self.executeClicksArray=np.sign(self.executeClicksArray) * np.ceil(np.abs(self.executeClicksArray))      
        self.executeClicksArray=self.executeClicksArray.astype(int)
        #print('calcClicksArray desided on =',self.executeClicksArray)
    def clickButtonsArray(self):
        self.currentClicksArray=np.add(self.currentClicksArray,self.executeClicksArray)
        if self.executeClicksArray[0]>0:
            self.clickButton('roll-right-button',np.absolute(self.executeClicksArray[0]),timeDeltaSameClicks)
        else: 
            self.clickButton('roll-left-button',np.absolute(self.executeClicksArray[0]),timeDeltaSameClicks)

        if self.executeClicksArray[1]>0:
            self.clickButton('pitch-down-button',np.absolute(self.executeClicksArray[1]),timeDeltaSameClicks)
        else: 
            self.clickButton('pitch-up-button',np.absolute(self.executeClicksArray[1]),timeDeltaSameClicks)

        if self.executeClicksArray[2]>0:
            self.clickButton('yaw-right-button',np.absolute(self.executeClicksArray[2]),timeDeltaSameClicks)
        else: 
            self.clickButton('yaw-left-button',np.absolute(self.executeClicksArray[2]),timeDeltaSameClicks)

        if self.executeClicksArray[4]>0:
            self.clickButton('translate-right-button',np.absolute(self.executeClicksArray[5]),timeDeltaSameClicks)
        else: 
            self.clickButton('translate-left-button',np.absolute(self.executeClicksArray[5]),timeDeltaSameClicks)

        if self.executeClicksArray[5]>0:
            self.clickButton('translate-up-button',np.absolute(self.executeClicksArray[4]),timeDeltaSameClicks)
        else: 
            self.clickButton('translate-down-button',np.absolute(self.executeClicksArray[4]),timeDeltaSameClicks)

        if self.executeClicksArray[6]>0:
            self.clickButton('translate-forward-button',np.absolute(self.executeClicksArray[6]),timeDeltaSameClicks)
        else: 
            self.clickButton('translate-backward-button',np.absolute(self.executeClicksArray[6]),timeDeltaSameClicks)
    def clickButton(self,buttonId,timesNum,timeDeltaSameClicks):
        self.buttonElement=browser.find_element_by_id(buttonId)
        for idx in range(timesNum):
            self.buttonElement.click()
            #time.sleep(timeDeltaSameClicks) #wait between consecutive clicks
    def printInstruments(self):
        print(self.currentErrorArray)
        print(self.currentRateArray)
        #printing Errors
        print('rollError =',self.currentErrorArray[0])
        print('pitchError =',self.currentErrorArray[1])
        print('yawError =',self.currentErrorArray[2])
        print('xError =',self.currentErrorArray[3])
        print('yError =',self.currentErrorArray[4])
        print('zError =',self.currentErrorArray[5])
        print('rangeError =',self.currentErrorArray[6])
        #printing Rates
        print('rollRate =',self.currentErrorArray[0])
        print('pitchRate =',self.currentErrorArray[1])
        print('yawError =',self.currentErrorArray[2])
        print('rangeRate =',self.currentErrorArray[6])

#array [roll, pitch, yaw, x, y, z, range]

#Parameters definition
timeDeltaSameClicks=0.1 #was 0.01
waitAfterButtonsClickable=5

#def main():
#chromedriver needs to be copied to disk
chromedriver = "E:\\MyProj\\chromedriver.exe"
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

controlPanel=controlPanelClass() # init controlPanelClass

#The loop
while 1:
    print('.... Running the loop ....')
    print('TheLoop: reading instruments ..')
    controlPanel.readInstruments()
    controlPanel.calcClicksArray()
    print('The loop: current clicks = ',controlPanel.currentClicksArray)
    print('TheLoop: executing clicks = ',controlPanel.executeClicksArray)
    controlPanel.clickButtonsArray()
    #print('desiredRateArray = currentErrorArray * rateParamsArray')
    #print(controlPanel.desiredRateArray[4],'=',controlPanel.currentErrorArray[4],'*',controlPanel.rateParamsArray[4])
    #print('deltaRateArray = desiredRateArray - currentRateArray')
    #print(controlPanel.deltaRateArray[4],'=',controlPanel.desiredRateArray[4],'-',controlPanel.currentRateArray[4])
    #print('clickExecute = ',controlPanel.executeClicksArray[4])
    #print('done')

    #TODO: bad current rate calculation - simply record number of clicks! and test click rate - easy!