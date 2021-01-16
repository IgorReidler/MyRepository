# Created by Igor Reidler
# May 2020
# github test 1.21

import numpy as np
import time
import datetime
import pause
import matplotlib.pyplot as plt
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
        self.rateParamsMaxArray=[2,2,2,10,10,10,10] #was [2,2,2,10,10,10,10]
        self.rateParamsMinArray=[-2,-2,-2,-10,-10,-10,-10] #was [-2,-2,-2,-10,-10,-10,-10]
        #self.rateParamsMaxArray=[1,1,1,3,3,3,10] #successful (but slow) was [1,1,1,1,1,1,2]
        #self.rateParamsMinArray=[-1,-1,-1,-3,-3,-3,-5] #successful (but slow) was [1,1,1,1,1,1,-2]
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
        self.rotationRateParam=0.8 #(success 0.8)
        self.translationRateParamXY=1 #last success with 1.0 
        self.translationRateParamZ=0.12  #last success with 0.035
        self.readInstrumentsTime=0.3
        self.desiredRateZarray=np.array([-12,-2,-0.05]) #31sec [-12,-2,-0.08]
        self.desiredMaxDistForRateZarray=np.array([10,3]) #31sec [10,2]

        #speed parameters
        self.translationRateParamZ=0.035 #(same as self.translationRateParamZ=0.035 was good)
        
        self.rateParamsArray=[self.rotationRateParam,self.rotationRateParam,self.rotationRateParam,-self.translationRateParamXY,-self.translationRateParamXY,-self.translationRateParamXY,-self.translationRateParamZ]
        self.ratePerClickArray=[self.ratePerClickRotation,self.ratePerClickRotation,self.ratePerClickRotation,self.ratePerClickTranslation,self.ratePerClickTranslation,self.ratePerClickTranslation,-self.ratePerClickTranslationZ]
        #array [roll, pitch, yaw, x, y, z, range]
    def readInstruments(self):
        self.readArray=browser.execute_script("return [camera.rotation.z,camera.rotation.x,camera.rotation.y,camera.position.x,camera.position.y,prevRange,rateRotationZ,rateRotationX,rateRotationY,rateCurrent,motionVector.x,motionVector.y];")
        self.currentErrorArray[0]  =float(self.readArray[0])*180/3.1415
        self.currentErrorArray[1]  =float(self.readArray[1])*180/3.1415
        self.currentErrorArray[2]  =float(self.readArray[2])*180/3.1415        
        self.currentErrorArray[4]  =float(self.readArray[3])     
        self.currentErrorArray[5]  =float(self.readArray[4])        
        self.currentErrorArray[6]  =float(self.readArray[5]) #range
        self.currentRateArray[0]    = self.readArray[6]/10
        self.currentRateArray[1]    = self.readArray[7]/10
        self.currentRateArray[2]    = self.readArray[8]/10        
        self.currentRateArray[6]    = self.readArray[9] #speed
        self.currentRateArray[4]    = self.readArray[10]*60
        self.currentRateArray[5]    = self.readArray[11]*60
    
    def dist2rate(self,range,desiredRateZarray,desiredMaxDistForRateZarray):
        if range > desiredMaxDistForRateZarray[0]:
            print('dist1')
            return desiredRateZarray[0]
        if desiredMaxDistForRateZarray[0] >= range >= desiredMaxDistForRateZarray[1]:
            print('dist2')
            return desiredRateZarray[1]
        if  desiredMaxDistForRateZarray[1] > range:
            print('dist3')
            return desiredRateZarray[2]
        return False #if did not succeed assigning

    def calcClicksArray(self):
        self.desiredRateArray=np.multiply(self.currentErrorArray,self.rateParamsArray)
        self.desiredRateArray[5]=self.desiredRateArray[5]+self.rateDeltaGravity #Gravity correction
        self.desiredRateArray[6]=self.dist2rate(self.currentErrorArray[6],self.desiredRateZarray,self.desiredMaxDistForRateZarray)
        self.deltaRateArray=np.subtract(self.desiredRateArray,self.currentRateArray)
        self.executeClicksArray=np.divide(self.deltaRateArray,self.ratePerClickArray)
        self.executeClicksArray=np.sign(self.executeClicksArray) * np.ceil(np.abs(self.executeClicksArray))
        self.executeClicksArray=self.executeClicksArray.astype(int)        
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
for gameNum in range(2):
    #Parameters definition
    waitAfterButtonsClickable=5

    #chromedriver
    chromedriver = r"E:\myproj\Python\chromedriver\chromedriver.exe"
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

    successElem=browser.find_element_by_id('success-button')
    failElem=browser.find_element_by_id('fail-button')
    #The loop
    loopStartTime=time.time()
    rangeZList=[]
    currentRateZList=[]
    desiredRateZList=[]
    rangeTimeList=[]
    while not (successElem.is_displayed() or failElem.is_displayed()):
        print('.... Running the loop ....')
        controlPanel.readInstruments() #Reading instruments
        currentRateZList.append(controlPanel.currentRateArray[6])
        rangeZList.append(controlPanel.currentErrorArray[6])
        print("Current rate = ", controlPanel.currentRateArray[6])
        desiredRateZList.append(controlPanel.desiredRateArray[6])
        rangeTimeList.append(round(time.time()-loopStartTime,2))
        controlPanel.calcClicksArray() #Calc clicks array
        controlPanel.clickButtonsArray() #Execute clicks array
    if successElem.is_displayed():
        loopTotalTime=time.time()-loopStartTime
        print('Total docking time =',round(loopTotalTime,2))
        writeString='Success!! '+'rotationRateParam='+str(controlPanel.rotationRateParam)+' translationRateParamZ='+str(controlPanel.translationRateParamZ)+' | Total docking time ='+str(round(loopTotalTime,2))+' seconds \n'
        print('Success!! translationRateParamXY=',controlPanel.translationRateParamXY,' translationRateParamXY=',controlPanel.translationRateParamZ)
        with open("iss_sim_autopylot_log.txt", "a") as f:
            f.write(writeString)
        loopTotalTime=time.time()-loopStartTime
    elif failElem.is_displayed():
        loopTotalTime=time.time()-loopStartTime
        print('Total docking time =',round(loopTotalTime,2))
        writeString='Fail!! '+'rotationRateParam='+str(controlPanel.rotationRateParam)+' translationRateParamZ='+str(controlPanel.translationRateParamZ)+' | Total docking time ='+str(round(loopTotalTime,2))+' seconds \n'
        print('Fail!! translationRateParamXY=',controlPanel.translationRateParamXY,' translationRateParamZ=',controlPanel.translationRateParamZ)
        with open("iss_sim_autopylot_log.txt", "a") as f:
            f.write(writeString)
    time.sleep(5)
    browser.close()
    
    fig, axs = plt.subplots(2)
    fig.suptitle('Stats')
    axs[0].plot(rangeTimeList[1:-20],rangeZList[1:-20])
    axs[1].plot(rangeTimeList[1:-20],currentRateZList[1:-20])
    axs[2].plot(rangeTimeList[1:-20],desiredRateZList[1:-20])

    plt.ylabel('Range from ISS (m)')
    plt.xlabel('Time (s))')
    svgName='range_'+time.strftime("%Y%m%d_%H%M%S")+'.svg'
    plt.savefig(svgName)
    plt.draw()
    plt.show()
plt.show()