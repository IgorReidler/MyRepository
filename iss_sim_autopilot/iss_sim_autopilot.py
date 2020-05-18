import numpy as np
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#TODO: max clicks should be total, not per executeClicks
#TODO: decisions log

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
        self.jsArray=['a','a','a','a','a','a','a']
        #self.jsArray = np.empty([7], dtype="S7")

        self.xyClicksParam=1 #was 1/3
        
        self.calcRatesFlag=1 #calculate translation rate from error (true) or from clicks (false)

        self.timeDeltaErrorUpdates=0
        self.timePrevErrorUpdate=0
        self.timeCurrentErrorUpdate=0
        self.firstreadInstruments=True
        self.ratePerClickRotation=0.1
        self.ratePerClickTranslation=0.06
        self.rateDeltaGravity=0.0098
        self.rotationRateParam=0.03
        self.translationRateParamXY=0.06 #was 0.015
        self.translationRateParamZ=0.015 #was 0.015
        self.rateParamsArray=[self.rotationRateParam,self.rotationRateParam,self.rotationRateParam,-self.translationRateParamXY,-self.translationRateParamXY,-self.translationRateParamXY,-self.translationRateParamZ]
        self.ratePerClickArray=[self.ratePerClickRotation,self.ratePerClickRotation,self.ratePerClickRotation,self.ratePerClickTranslation,self.ratePerClickTranslation,self.ratePerClickTranslation,-self.translationRateParamZ]
        #array [roll, pitch, yaw, x, y, z, range]

    def readInstruments(self):
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
        #Rotation Rates read
        self.currentRateArray[0]  =float(browser.find_element_by_xpath("//div[@id='roll']/div[contains(@class, 'rate')]").text[:-3])
        self.currentRateArray[1]  =float(browser.find_element_by_xpath("//div[@id='pitch']/div[contains(@class, 'rate')]").text[:-3])
        self.currentRateArray[2]  =float(browser.find_element_by_xpath("//div[@id='yaw']/div[contains(@class, 'rate')]").text[:-3])
        #Translation Rates read
        self.currentRateArray[6] = float(browser.find_element_by_xpath("//div[@id='rate']/div[contains(@class, 'rate')]").text[:-4])
        #Translation Rates calc

        if self.calcRatesFlag:
            #Calculate y, z rates
            if not self.firstreadInstruments:
                self.timeDeltaErrorUpdates = self.timeCurrentErrorUpdate - self.timePrevErrorUpdate
                self.currentRateArray[4:6]=np.subtract(self.currentErrorArray[4:6],self.previousErrorArray[4:6])
                self.currentRateArray[4:6]=np.divide(self.currentRateArray[4:6],self.timeDeltaErrorUpdates)
            self.firstreadInstruments=False
        #else:
        #    self.currentRateArray[4] = np.multiply(self.currentClicksArray[4],self.ratePerClickTranslation)
        #    self.currentRateArray[5] = np.multiply(self.currentClicksArray[5],self.ratePerClickTranslation) #-0.01to account for gravity

    def calcClicksArray(self):
        if self.calcRatesFlag:
            #self.desiredRateArray=np.power(self.currentErrorArray,2)
            self.desiredRateArray=np.multiply(self.currentErrorArray,self.rateParamsArray)
            self.desiredRateArray[5]=self.desiredRateArray[5]+self.rateDeltaGravity #Gravity correction
            self.deltaRateArray=np.subtract(self.desiredRateArray,self.currentRateArray)
            self.executeClicksArray=np.divide(self.deltaRateArray,self.ratePerClickArray)
            self.executeClicksArray=np.clip(self.executeClicksArray,-10,10)
            self.executeClicksArray=np.sign(self.executeClicksArray) * np.ceil(np.abs(self.executeClicksArray))      
            #self.clicksExecuteArray=np.ceil(self.clicksExecuteArray) #was around
            self.executeClicksArray=self.executeClicksArray.astype(int)
            #print('calcClicksArray desided on =',self.clicksExecuteArray)
        #else:
        #    #self.desiredRateArray=np.power(self.currentErrorArray,2) #for power law rate
        #    #rate calculation for rotations
        #    self.desiredRateArray[0:3]=np.multiply(self.currentErrorArray[0:3],self.rateParamsArray[0:3])
        #    self.deltaRateArray[0:3]=np.subtract(self.desiredRateArray[0:3],self.currentRateArray[0:3])
        #    self.executeClicksArray[0:3]=np.divide(self.deltaRateArray[0:3],self.ratePerClickArray[0:3][0:3])
        #    self.executeClicksArray[0:3]=np.clip(self.executeClicksArray[0:3],-10,10)
        #    #direct calculation for x,y
        #    self.desiredClicksArray[4:6]=np.ceil(np.multiply(self.currentErrorArray[4:6],-self.xyClicksParam))
        #    self.executeClicksArray[4:6]=np.subtract(self.desiredClicksArray[4:6],self.currentClicksArray[4:6])
        #    #general clip, ceil, int
        #    self.executeClicksArray=np.sign(self.executeClicksArray) * np.ceil(np.abs(self.executeClicksArray))      
        #    self.executeClicksArray=self.executeClicksArray.astype(int)
        #    #print('calcClicksArray desided on =',self.executeClicksArray)

    def clickButtonsArray(self):
        self.currentClicksArray=np.add(self.currentClicksArray,self.executeClicksArray)
        if self.executeClicksArray[0]>=0:
            #self.clickButton('roll-right-button',np.absolute(self.executeClicksArray[0]),timeDeltaSameClicks)
            self.jsArray[0]='rollRight();'
        else: 
            #self.clickButton('roll-left-button',np.absolute(self.executeClicksArray[0]),timeDeltaSameClicks)
            self.jsArray[0]='rollLeft();'

        if self.executeClicksArray[1]>=0:
            #self.clickButton('pitch-down-button',np.absolute(self.executeClicksArray[1]),timeDeltaSameClicks)
            self.jsArray[1]='pitchDown();'
        else: 
            #self.clickButton('pitch-up-button',np.absolute(self.executeClicksArray[1]),timeDeltaSameClicks)
            self.jsArray[1]='pitchUp();'
        if self.executeClicksArray[2]>=0:
            #self.clickButton('yaw-right-button',np.absolute(self.executeClicksArray[2]),timeDeltaSameClicks)
            self.jsArray[2]='yawRight();'
        else: 
            #self.clickButton('yaw-left-button',np.absolute(self.executeClicksArray[2]),timeDeltaSameClicks)
            self.jsArray[2]='yawLeft();'
        self.jsArray[3]='' #to fill the unused x translation
        if self.executeClicksArray[4]>=0:
            #self.clickButton('translate-right-button',np.absolute(self.executeClicksArray[4]),timeDeltaSameClicks*10)
            self.jsArray[4]='translateRight();'
        else: 
           # self.clickButton('translate-left-button',np.absolute(self.executeClicksArray[4]),timeDeltaSameClicks*10)
            self.jsArray[4]='translateLeft();'
#       
        if self.executeClicksArray[5]>=0:
           # self.clickButton('translate-up-button',np.absolute(self.executeClicksArray[5]),timeDeltaSameClicks)
            self.jsArray[5]='translateUp();'
        else: 
           # self.clickButton('translate-down-button',np.absolute(self.executeClicksArray[5]),timeDeltaSameClicks)
            self.jsArray[5]='translateDown();'
#
        if self.executeClicksArray[6]>=0:
          #  self.clickButton('translate-forward-button',np.absolute(self.executeClicksArray[6]),timeDeltaSameClicks)
            self.jsArray[6]='translateForward();'
        else: 
          #  self.clickButton('translate-backward-button',np.absolute(self.executeClicksArray[6]),timeDeltaSameClicks)
            self.jsArray[6]='translateBackward();'
        # following replaces clickButton() function
        self.executeClicksArray=np.absolute(self.executeClicksArray)
        self.jsExecuteString=(self.jsArray[0])*self.executeClicksArray[0]+(self.jsArray[1])*self.executeClicksArray[1]+(self.jsArray[2])*self.executeClicksArray[2]+(self.jsArray[3])*self.executeClicksArray[3]+(self.jsArray[4])*self.executeClicksArray[4]+(self.jsArray[5])*self.executeClicksArray[5]+(self.jsArray[6])*self.executeClicksArray[6]
        print(self.jsExecuteString)
        browser.execute_script(self.jsExecuteString)
    def clickButton(self,buttonId,timesNum,timeDeltaSameClicks):
        self.buttonElement=browser.find_element_by_id(buttonId)
        for idx in range(int(timesNum)):
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
timeDeltaSameClicks=0.00 #was 0.01
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
print('Clicked the large "Begin" button')
elem.click()
#print('Click the large "Begin" button to continue!')




#wait for translate-up-button to become clickable
wait = WebDriverWait(browser, 1000)
wait.until(EC.element_to_be_clickable((By.ID, 'translate-up-button')))
time.sleep(waitAfterButtonsClickable)
print('<<<<<<<<<<<< Script is Ready! >>>>>>>>>>>>>')

controlPanel=controlPanelClass() # init controlPanelClass

#The loop
while 1:
    print('.... Running the loop ....')
    #print('TheLoop: reading instruments ..')
    controlPanel.readInstruments()
    controlPanel.calcClicksArray()
    
    print('The loop: current error  = ',controlPanel.currentErrorArray[4:6])
    print('The loop: current rate   = ',str.format('{0:.4f}', controlPanel.currentRateArray[4]),' and ',str.format('{0:.4f}', controlPanel.currentRateArray[5]))
    print('The loop: desired rate   = ',str.format('{0:.4f}', controlPanel.desiredRateArray[4]),' and ',str.format('{0:.4f}', controlPanel.desiredRateArray[5]))
    print('The loop: time delta     = ',str.format('{0:.2f}', controlPanel.timeDeltaErrorUpdates))
    print('The Loop: desired clicks = ',controlPanel.executeClicksArray[4:6])
    print('The loop: current clicks = ',controlPanel.currentClicksArray[4:6])
    controlPanel.clickButtonsArray()
    #time.sleep(3)

    #print('desiredRateArray = currentErrorArray * rateParamsArray')
    #print(controlPanel.desiredRateArray[4],'=',controlPanel.currentErrorArray[4],'*',controlPanel.rateParamsArray[4])
    #print('deltaRateArray = desiredRateArray - currentRateArray')
    #print(controlPanel.deltaRateArray[4],'=',controlPanel.desiredRateArray[4],'-',controlPanel.currentRateArray[4])
    #print('clickExecute = ',controlPanel.executeClicksArray[4])
    #print('done')