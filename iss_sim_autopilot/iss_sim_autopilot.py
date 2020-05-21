# Created by Igor Reidler
# May 2020
# github test 1.21

import numpy as np
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#TODO: asyncio + plan desired error delta, rate amplitude and duration
# consider using fixed amplitude, changing only duration.

#Comment: what is motionVector?

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
        self.jsArray=['a','a','a','a','a','a','a'] #init js array
        self.rateParamsMaxArray=[1,1,1,3,3,3,5] #successful (but slow) was [1,1,1,1,1,1,2]
        self.rateParamsMinArray=[-1,-1,-1,-3,-3,-3,-5] #successful (but slow) was [1,1,1,1,1,1,-2]
        #self.jsArray = np.empty([7], dtype="S7")
        self.xyClicksParam=1 #was 1/3
        self.timeFlag=0

        self.calcRatesFlag=1 #calculate translation rate from error (true) or from clicks (false)

        self.timeDeltaErrorUpdates=0
        self.timePrevErrorUpdate=0
        self.timeCurrentErrorUpdate=0
        self.firstreadInstruments=True
        self.ratePerClickRotation=0.1
        self.ratePerClickTranslation=0.06
        self.ratePerClickTranslationZ=0.045
        self.rateDeltaGravity=0.0000 #was 0.0098 (0 is correct)
        self.rotationRateParam=0.03
        self.translationRateParamXY=0.06 #last success with 0.06
        self.translationRateParamZ=0.045  #last success with 0.045
        self.rateParamsArray=[self.rotationRateParam,self.rotationRateParam,self.rotationRateParam,-self.translationRateParamXY,-self.translationRateParamXY,-self.translationRateParamXY,-self.translationRateParamZ]
        self.ratePerClickArray=[self.ratePerClickRotation,self.ratePerClickRotation,self.ratePerClickRotation,self.ratePerClickTranslation,self.ratePerClickTranslation,self.ratePerClickTranslation,-self.ratePerClickTranslationZ]
        #array [roll, pitch, yaw, x, y, z, range]
    def readInstruments(self):
        try:
            if self.timeFlag: self.readInstrumentsTimeStart=time.time()
            self.readInstrumentsTimeStart=time.time()
            self.previousErrorArray=np.copy(self.currentErrorArray) #save last current error array to previous
            self.timePrevErrorUpdate = self.timeCurrentErrorUpdate #save last current time array to previous
            self.currentErrorArray[0] = float(browser.execute_script("return fixedRotationZ;"))
            self.currentErrorArray[1] = float(browser.execute_script("return fixedRotationX;"))
            self.currentErrorArray[2] = float(browser.execute_script("return fixedRotationY;"))         
            #Translation Error
            self.currentErrorArray[3]  =float(browser.find_element_by_xpath("//div[@id='x-range']/div[@class='distance']").text[:-1])
            self.currentErrorArray[4]  =float(browser.find_element_by_xpath("//div[@id='y-range']/div[@class='distance']").text[:-1])
            self.timeCurrentErrorUpdate = time.time()
            self.currentErrorArray[5]  =float(browser.find_element_by_xpath("//div[@id='z-range']/div[@class='distance']").text[:-1])
            self.currentErrorArray[6] = float(browser.execute_script("return prevRange;"))          
            if self.timeFlag: self.readInstrumentsTimeErrorsFinished=time.time()
            #Rotation Rates read
            self.currentRateArray[0]  = browser.execute_script("return rateRotationZ/10;")
            self.currentRateArray[1] = browser.execute_script("return rateRotationX/10;")
            self.currentRateArray[2] = browser.execute_script("return rateRotationY/10;")           
            #Translation Rates read
            self.currentRateArray[6] = browser.execute_script("return rateCurrent;")
            if self.timeFlag: self.readInstrumentsTimeRatesFinished=time.time()
            #Translation Rates calc         
            #Calculate y, z rates
            if not self.firstreadInstruments:
                self.timeDeltaErrorUpdates = self.timeCurrentErrorUpdate - self.timePrevErrorUpdate
                self.currentRateArray[4:6]=np.subtract(self.currentErrorArray[4: 6],self.previousErrorArray[4:6])
                self.currentRateArray[4:6]=np.divide(self.currentRateArray[4:6],self.timeDeltaErrorUpdates)
            self.firstreadInstruments=False

            if self.timeFlag: self.calcZtimes=time.time()
        except:
            print('Docking simulation ended')
            self.dockingTotalTime=time.time()-dockingStartTime
            print('Total docking time =',round(self.dockingTotalTime,2))
            self.runFlag=0
            exit()

    def calcClicksArray(self):
        #self.desiredRateArray=np.power(self.currentErrorArray,2)
        self.desiredRateArray=np.multiply(self.currentErrorArray,self.rateParamsArray)
        self.desiredRateArray[5]=self.desiredRateArray[5]+self.rateDeltaGravity #Gravity correction
        self.desiredRateArray=np.clip(self.desiredRateArray,self.rateParamsMinArray,self.rateParamsMaxArray)
        self.deltaRateArray=np.subtract(self.desiredRateArray,self.currentRateArray)
        self.executeClicksArray=np.divide(self.deltaRateArray,self.ratePerClickArray)
        #self.executeClicksArray=np.clip(self.executeClicksArray,-10,10) #replaced by rate clipping
        self.executeClicksArray=np.sign(self.executeClicksArray) * np.ceil(np.abs(self.executeClicksArray))
        #self.clicksExecuteArray=np.ceil(self.clicksExecuteArray) #was around
        self.executeClicksArray=self.executeClicksArray.astype(int)
        #self.elapsedTime=self.readInstrumentsTimeEnd=time.time()-self.readInstrumentsTimeStart
        #print(self.elapsedTime)

        #Big red button
        self.currentErrorArrayAbs=np.absolute(self.currentErrorArray)
        if self.currentErrorArrayAbs[0]<0.1 and self.currentErrorArrayAbs[1]<0.1 and self.currentErrorArrayAbs[2]<0.1 and self.currentErrorArrayAbs[3]<0.4 and self.currentErrorArrayAbs[4]<0.2 and self.currentErrorArrayAbs[5]<0.2:
              self.executeClicksArray=[0,0,0,0,0,0,3]
              #self.translationRateParamZ=0.1
              print('Big red button activated!!!!!!!!!!!!!!!!!!!')

    def clickButtonsArray(self):
        self.currentClicksArray=np.add(self.currentClicksArray,self.executeClicksArray)
        if self.executeClicksArray[0]>=0:
            self.jsArray[0]='rollRight();'
        else: 
            self.jsArray[0]='rollLeft();'

        if self.executeClicksArray[1]>=0:
            self.jsArray[1]='pitchDown();'
        else: 
            self.jsArray[1]='pitchUp();'

        if self.executeClicksArray[2]>=0:
            self.jsArray[2]='yawRight();'
        else: 
            self.jsArray[2]='yawLeft();'

        self.jsArray[3]='' #to fill the unused x translation

        if self.executeClicksArray[4]>=0:
            self.jsArray[4]='translateRight();'
        else: 
            self.jsArray[4]='translateLeft();'
#       
        if self.executeClicksArray[5]>=0:
            self.jsArray[5]='translateUp();'
        else: 
            self.jsArray[5]='translateDown();'
#
        if self.executeClicksArray[6]>=0:
            self.jsArray[6]='translateForward();'
        else: 
            self.jsArray[6]='translateBackward();'

        #creating a long javaScript commands string
        self.executeClicksArray=np.absolute(self.executeClicksArray) #number of times a string is pasted must be positive
        self.jsExecuteString=(self.jsArray[0])*self.executeClicksArray[0]+(self.jsArray[1])*self.executeClicksArray[1]+(self.jsArray[2])*self.executeClicksArray[2]+(self.jsArray[3])*self.executeClicksArray[3]+(self.jsArray[4])*self.executeClicksArray[4]+(self.jsArray[5])*self.executeClicksArray[5]+(self.jsArray[6])*self.executeClicksArray[6]
        browser.execute_script(self.jsExecuteString) #execute the string

#array [roll, pitch, yaw, x, y, z, range]

#Parameters definition
timeDeltaSameClicks=0.00 #was 0.01
waitAfterButtonsClickable=5

#chromedriver
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
dockingStartTime=time.time()

controlPanel=controlPanelClass() # init controlPanelClass

#The loop
while 1:
    print('.... Running the loop ....')
    #print('TheLoop: reading instruments ..')
    startTime=time.time()
    controlPanel.readInstruments()
    readInstrumentsTime=time.time()
    #print('Current error  = ',controlPanel.currentErrorArray)
    #print('Current rate   = ',controlPanel.currentRateArray)
    #print('Desired rate   = ',controlPanel.desiredRateArray)
    ##print('Time delta     = ',str.format('{0:.2f}', controlPanel.timeDeltaErrorUpdates))
    #print('Desired clicks = ',controlPanel.executeClicksArray)
    #print('Current clicks = ',controlPanel.currentClicksArray)
    #print('Executing clicks = ',controlPanel.executeClicksArray)
    controlPanel.calcClicksArray()
    calcClicksTime=time.time()
    controlPanel.clickButtonsArray()
    clickButtonsTime=time.time()
    if controlPanel.timeFlag: print('ReadInstruments Time Js = ',round(controlPanel.readInstrumentsTimeErrorsFinished-controlPanel.readInstrumentsTimeStart,2))
    if controlPanel.timeFlag: print('ReadInstruments Time Xpath = ',round(controlPanel.readInstrumentsTimeRatesFinished-controlPanel.readInstrumentsTimeErrorsFinished,2))
    if controlPanel.timeFlag: print('ReadInstruments Time calcZ = ',round(controlPanel.calcZtimes-controlPanel.readInstrumentsTimeRatesFinished,2))
    print('Total ReadInstruments Time = ',round(readInstrumentsTime-startTime,2))
    print('calcClicks Time = ',round(calcClicksTime-readInstrumentsTime,2))
    print('clickButtons Time = ',round(clickButtonsTime-calcClicksTime,2))