import numpy as np
import time
from timeloop import Timeloop
from datetime import timedelta

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#comment for github

class controlPanelClass(): 
    def __init__(self): 
        self.currentErrorArray=np.zeros(7)
        self.previousErrorArray=np.zeros(7)
        self.currentRateArray=np.zeros(7)
        self.desiredRateArray=np.zeros(7)
        self.deltaRateArray=np.zeros(7)
        self.desiredClicksArray=np.zeros(7)
        self.clicksExecuteArray=np.zeros(7)
        self.rateParamsArray=np.zeros(7)
        self.ratePerClickArray=np.zeros(7)

        self.timeDeltaErrorUpdates=0
        self.timePrevErrorUpdate=0
        self.timeCurrentErrorUpdate=0
        self.firstreadInstruments=True
        self.ratePerClickRotation=0.1
        self.ratePerClickTranslation=0.05
        self.rateGravity=0.0065
        self.rotationRateParam=0.03
        self.translationRateParam=0.015
        self.rateParamsArray=[self.rotationRateParam,self.rotationRateParam,self.rotationRateParam,-self.translationRateParam,-self.translationRateParam,-self.translationRateParam,-self.translationRateParam]
        self.ratePerClickArray=[self.ratePerClickRotation,self.ratePerClickRotation,self.ratePerClickRotation,self.ratePerClickTranslation,self.ratePerClickTranslation,self.ratePerClickTranslation,-self.translationRateParam]
        #array [roll, pitch, yaw, x, y, z, range]

    #def reset(self):
    #    self.currentErrorArray=np.zeros(7)
    #    self.currentRateArray=np.zeros(7)
    #    self.desiredRateArray=np.zeros(7)
    #    self.desiredClicksArray=np.zeros(7)
    #    self.currentClicksArray=np.zeros(7).astype(int)
    #    self.clicksExecuteArray=np.zeros(7)

    def readInstruments(self):
        print('[[[[[[ Reading instruments ]]]]]')
        self.previousErrorArray=np.copy(self.currentErrorArray) #save last current error array to previous
        self.timePrevErrorUpdate = self.timeCurrentErrorUpdate #save last current time array to previous
        self.currentErrorArray[0] = float(browser.find_element_by_xpath("//div[@id='roll']/div[@class='error']").text[:-1])
        self.currentErrorArray[1]  =float(browser.find_element_by_xpath("//div[@id='pitch']/div[@class='error']").text[:-1])
        self.currentErrorArray[2]  =float(browser.find_element_by_xpath("//div[@id='yaw']/div[@class='error']").text[:-1])
        #Translation Error
        self.currentErrorArray[3]  =float(browser.find_element_by_xpath("//div[@id='x-range']/div[@class='distance']").text[:-1])
        self.timeCurrentErrorUpdate = time.time()
        self.currentErrorArray[4]  =float(browser.find_element_by_xpath("//div[@id='y-range']/div[@class='distance']").text[:-1])
        self.currentErrorArray[5]  =float(browser.find_element_by_xpath("//div[@id='z-range']/div[@class='distance']").text[:-1])
        self.currentErrorArray[6]  =float(browser.find_element_by_xpath("//div[@id='range']/div[@class='rate']").text[:-1])
        #Rotation Rates
        self.currentRateArray[0]  =float(browser.find_element_by_xpath("//div[@id='roll']/div[contains(@class, 'rate')]").text[:-3])
        self.currentRateArray[1]  =float(browser.find_element_by_xpath("//div[@id='pitch']/div[contains(@class, 'rate')]").text[:-3])
        self.currentRateArray[2]  =float(browser.find_element_by_xpath("//div[@id='yaw']/div[contains(@class, 'rate')]").text[:-3])
        #Translation Rates
        self.currentRateArray[6] = float(browser.find_element_by_xpath("//div[@id='rate']/div[contains(@class, 'rate')]").text[:-4])
        #Calculate y, z rates
        if not self.firstreadInstruments:
            self.timeDeltaErrorUpdates = self.timeCurrentErrorUpdate - self.timePrevErrorUpdate
            print('time Delta = ',self.timeDeltaErrorUpdates)
            self.currentRateArray[4]=np.subtract(self.currentErrorArray[4],self.previousErrorArray[4])
            self.currentRateArray[4]=np.divide(self.currentRateArray[4],self.timeDeltaErrorUpdates)
            print('Rate = ',self.currentRateArray[4])

        self.firstreadInstruments=False
    def calcClicksArray(self):
        #self.desiredRateArray=np.power(self.currentErrorArray,2)
        self.desiredRateArray=np.multiply(self.currentErrorArray,self.rateParamsArray)
        self.deltaRateArray=np.subtract(self.desiredRateArray,self.currentRateArray)
        self.clicksExecuteArray=np.divide(self.deltaRateArray,self.ratePerClickArray)
        self.clicksExecuteArray=np.clip(self.clicksExecuteArray,-10,10)
        self.clicksExecuteArray=np.sign(self.clicksExecuteArray) * np.ceil(np.abs(self.clicksExecuteArray))      
        #self.clicksExecuteArray=np.ceil(self.clicksExecuteArray) #was around
        self.clicksExecuteArray=self.clicksExecuteArray.astype(int)
        #print('calcClicksArray desided on =',self.clicksExecuteArray)
    def clickButtonsArray(self):
        print('clickButtonsArray received =',self.clicksExecuteArray)
        if self.clicksExecuteArray[0]>0:
            self.clickButton('roll-right-button',np.absolute(self.clicksExecuteArray[0]),timeDeltaSameClicks)
        else: 
            self.clickButton('roll-left-button',np.absolute(self.clicksExecuteArray[0]),timeDeltaSameClicks)
#
        if self.clicksExecuteArray[1]>0:
            self.clickButton('pitch-down-button',np.absolute(self.clicksExecuteArray[1]),timeDeltaSameClicks)
        else: 
            self.clickButton('pitch-up-button',np.absolute(self.clicksExecuteArray[1]),timeDeltaSameClicks)
#
        if self.clicksExecuteArray[2]>0:
            self.clickButton('yaw-right-button',np.absolute(self.clicksExecuteArray[2]),timeDeltaSameClicks)
        else: 
            self.clickButton('yaw-left-button',np.absolute(self.clicksExecuteArray[2]),timeDeltaSameClicks)

        if self.clicksExecuteArray[4]>0:
            self.clickButton('translate-right-button',np.absolute(self.clicksExecuteArray[4]),timeDeltaSameClicks)
        else: 
            self.clickButton('translate-left-button',np.absolute(self.clicksExecuteArray[4]),timeDeltaSameClicks)
##
        if self.clicksExecuteArray[5]>0:
            self.clickButton('translate-up-button',np.absolute(self.clicksExecuteArray[5]),timeDeltaSameClicks)
        else: 
            self.clickButton('translate-down-button',np.absolute(self.clicksExecuteArray[5]),timeDeltaSameClicks)
##
        #if self.clicksExecuteArray[6]>0:
        #    self.clickButton('translate-backward-button',np.absolute(self.clicksExecuteArray[6]),timeDeltaSameClicks)
        #else: 
        #    self.clickButton('translate-forward-button',np.absolute(self.clicksExecuteArray[6]),timeDeltaSameClicks)
        print('skip clicks')
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

#Class init
controlPanel=controlPanelClass()
#First read check
controlPanel.readInstruments()
controlPanel.printInstruments()

##scheduler
#s = sched.scheduler(time.time, time.sleep)
#def do_something(sc): 
#    print(".... Running the loop ....")
#    controlPanel.readInstruments()
#    controlPanel.calcClicksArray()
#    controlPanel.clickButtonsArray()
#    # do your stuff
#    s.enter(5, 1, do_something, (sc,))
#s.enter(5, 1, do_something, (s,))
#s.run()

#The loop
tl = Timeloop()
@tl.job(interval=timedelta(seconds=1))
def sample_job_every_5s():
    print("Job current time = {}".format(time.ctime()))
    controlPanel.readInstruments()
    controlPanel.calcClicksArray()
    #print('desiredRateArray = currentErrorArray * rateParamsArray')
    #print(controlPanel.desiredRateArray[4],'=',controlPanel.currentErrorArray[4],'*',controlPanel.rateParamsArray[4])
    #print('deltaRateArray = desiredRateArray - currentRateArray')
    #print(controlPanel.deltaRateArray[4],'=',controlPanel.desiredRateArray[4],'-',controlPanel.currentRateArray[4])
    #print('clickExecute = ',controlPanel.clicksExecuteArray[4])
    #print('done')
    controlPanel.clickButtonsArray()

    #TODO: bad current rate calculation - simply record number of clicks! and test click rate - easy!

    #print('previousErrorArray = ',self.previousErrorArray[4])
    #print('currentErrorArray = ',self.currentErrorArray[4])
    #print('currentRateArray = ',self.currentRateArray[4])
    #print('time delta = ',self.timeDeltaErrorUpdates)
    #print('done')

tl.start(block=True)
