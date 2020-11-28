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
        self.rotationRateParam=0.06 #(success 0.03)
        self.translationRateParamXY=0.2 #last success with 0.06 (Sep2020 0.5)
        self.translationRateParamZ=0.035  #last success with 0.035
        self.readInstrumentsTime=0.3
        
        #speed parameters
        self.gearShiftDistance=5 #distance at which to switch between translationRateParamZfast and translationRateParamZslow
        self.translationRateParamZfast=0.07
        self.translationRateParamZslow=0.05 #(same as self.translationRateParamZ=0.035 was good)
        
        self.rateParamsArray=[self.rotationRateParam,self.rotationRateParam,self.rotationRateParam,-self.translationRateParamXY,-self.translationRateParamXY,-self.translationRateParamXY,-self.translationRateParamZ]
        self.ratePerClickArray=[self.ratePerClickRotation,self.ratePerClickRotation,self.ratePerClickRotation,self.ratePerClickTranslation,self.ratePerClickTranslation,self.ratePerClickTranslation,-self.ratePerClickTranslationZ]
        #array [roll, pitch, yaw, x, y, z, range]
    def readInstruments(self):
        readStartTime = datetime.datetime.today()
        readEndTime = readStartTime + datetime.timedelta(0,self.readInstrumentsTime) # days, seconds, then other fields.
    #try:
        #self.readInstrumentsTimeStart=time.time()
        #self.previousErrorArray=np.copy(self.currentErrorArray) #save last current error array to previous
        #self.timePrevErrorUpdate = self.timeCurrentErrorUpdate #save last current time array to previous
        #self.currentErrorArray[0] = float(browser.execute_script("return fixedRotationZ;"))
        #self.currentErrorArray[1] = float(browser.execute_script("return fixedRotationX;"))
        #self.currentErrorArray[2] = float(browser.execute_script("return fixedRotationY;"))
        self.readArray=browser.execute_script("return [camera.rotation.z,camera.rotation.x,camera.rotation.y,camera.position.x,camera.position.y,prevRange,rateRotationZ,rateRotationX,rateRotationY,rateCurrent,motionVector.x,motionVector.y];")
        self.currentErrorArray[0]  =float(self.readArray[0])*180/3.1415
        self.currentErrorArray[1]  =float(self.readArray[1])*180/3.1415
        self.currentErrorArray[2]  =float(self.readArray[2])*180/3.1415        
        self.currentErrorArray[4]  =float(self.readArray[3])     
        self.currentErrorArray[5]  =float(self.readArray[4])        
        self.currentErrorArray[6]  =float(self.readArray[5])
        self.currentRateArray[0]    = self.readArray[6]/10
        self.currentRateArray[1]    = self.readArray[7]/10
        self.currentRateArray[2]    = self.readArray[8]/10        
        self.currentRateArray[6]    = self.readArray[9]
        self.currentRateArray[4]    = self.readArray[10]*60
        self.currentRateArray[5]    = self.readArray[11]*60
        #Translation Error
        #self.currentErrorArray[3]  =float(browser.find_element_by_xpath("//div[@id='x-range']/div[@class='distance']").text[:-1])
        #self.currentErrorArray[4]  =float(browser.find_element_by_xpath("//div[@id='y-range']/div[@class='distance']").text[:-1])
        ##self.currentErrorArray[4]  =float(browser.execute_script("return camera.position.x;")) 
        #self.timeCurrentErrorUpdate = time.time()
        #self.currentErrorArray[5]  =float(browser.find_element_by_xpath("//div[@id='z-range']/div[@class='distance']").text[:-1])
        ##self.currentErrorArray[5]  =float(browser.execute_script("return camera.position.y;")) 
        ##self.currentErrorArray[6] = float(browser.execute_script("return prevRange;"))          
        #if self.timeFlag: self.readInstrumentsTimeErrorsFinished=time.time()
        #Rotation Rates read
        #self.currentRateArray[0]  = browser.execute_script("return rateRotationZ/10;")
        #self.currentRateArray[1] = browser.execute_script("return rateRotationX/10;")
        #self.currentRateArray[2] = browser.execute_script("return rateRotationY/10;")           
        #Translation Rates read
        ##self.currentRateArray[6] = browser.execute_script("return rateCurrent;")
        #if self.timeFlag: self.readInstrumentsTimeRatesFinished=time.time()
        #Translation Rates calc         
        ##self.currentRateArray[4]  = browser.execute_script("return motionVector.x*60;")
        ##self.currentRateArray[5]  = browser.execute_script("return motionVector.y*60;")
        #print('rate m =',round(self.currentRateArray[4],3),' ',round(self.currentRateArray[5],3))
        
        ##pause.until(readEndTime)
        
        #exit()

    def calcClicksArray(self):
        #self.desiredRateArray=np.power(self.currentErrorArray,2)
        #print('Using translationRateParamZ='+str(self.rateParamsArray[6]))
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
        
        #self.executeClicksArray[3:7]=[0,0,0,0] #to only click rotation
        
        ##Big red button
        #self.currentErrorArrayAbs=np.absolute(self.currentErrorArray)
        #if self.currentErrorArrayAbs[0]<0.1 and self.currentErrorArrayAbs[1]<0.1 and self.currentErrorArrayAbs[2]<0.1 and self.currentErrorArrayAbs[3]<0.4 and self.currentErrorArrayAbs[4]<0.2 and self.currentErrorArrayAbs[5]<0.2:
        #      self.executeClicksArray=[0,0,0,0,0,0,3]
        #      #self.translationRateParamZ=0.1
        #      print('Big red button activated!!!!!!!!!!!!!!!!!!!')

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
for gameNum in range(10):
    #Parameters definition
    timeDeltaSameClicks=0.00 #was 0.01
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
    rangeTimeList=[]
    while not (successElem.is_displayed() or failElem.is_displayed()):
        print('.... Running the loop ....')
        #print('TheLoop: reading instruments ..')
        startTime=time.time()
        controlPanel.readInstruments()
        time1=time.time()
        if controlPanel.currentErrorArray[6]>controlPanel.gearShiftDistance:
            controlPanel.rateParamsArray[6]=-controlPanel.translationRateParamZfast
            #controlPanel.translationRateParamZ=controlPanel.translationRateParamZfast
        else:
            controlPanel.rateParamsArray[6]=-controlPanel.translationRateParamZslow
        #print('translation rate param Z  = ',controlPanel.translationRateParamZ)
        rangeZList.append(controlPanel.currentErrorArray[6])
        rangeTimeList.append(round(time.time()-loopStartTime,2))
        #print('Current error  = ',controlPanel.currentErrorArray)
        #print('Current rate   = ',controlPanel.currentRateArray)
        #print('Desired rate   = ',controlPanel.desiredRateArray)
        #print('Desired clicks = ',controlPanel.executeClicksArray)
        #print('Current clicks = ',controlPanel.currentClicksArray)
        #print('Executing clicks = ',controlPanel.executeClicksArray)
        time2=time.time()
        controlPanel.calcClicksArray()
        time3=time.time()
        controlPanel.clickButtonsArray()
        time4=time.time()
        #if controlPanel.timeFlag: print('ReadInstruments Time Js = ',round(controlPanel.readInstrumentsTimeErrorsFinished-controlPanel.readInstrumentsTimeStart,2))
        #if controlPanel.timeFlag: print('ReadInstruments Time Xpath = ',round(controlPanel.readInstrumentsTimeRatesFinished-controlPanel.readInstrumentsTimeErrorsFinished,2))
        #if controlPanel.timeFlag: print('ReadInstruments Time calcZ = ',round(controlPanel.calcZtimes-controlPanel.readInstrumentsTimeRatesFinished,2))
        print('Total ReadInstruments Time   = ',round(time1-startTime,2))
        print('Stuff time                   = ',round(time2-time1,2))
        print('calcClicks time              = ',round(time3-time2,2))
        print('clickButtons Time            = ',round(time4-time3,2))
    if successElem.is_displayed():
        loopTotalTime=time.time()-loopStartTime
        print('Total docking time =',round(loopTotalTime,2))
        writeString='Success!! '+'rotationRateParam='+str(controlPanel.rotationRateParam)+' translationRateParamZfast='+str(controlPanel.translationRateParamZfast)+' translationRateParamZslow='+str(controlPanel.translationRateParamZslow)+' gearShiftDistance='+str(controlPanel.gearShiftDistance)+' | Total docking time ='+str(round(loopTotalTime,2))+' seconds \n'
        print('Success!! translationRateParamXY=',controlPanel.translationRateParamXY,' translationRateParamXY=',controlPanel.translationRateParamZ)
        with open("iss_sim_autopylot_log.txt", "a") as f:
            f.write(writeString)
        loopTotalTime=time.time()-loopStartTime
    elif failElem.is_displayed():
        loopTotalTime=time.time()-loopStartTime
        print('Total docking time =',round(loopTotalTime,2))
        writeString='Fail!! '+'rotationRateParam='+str(controlPanel.rotationRateParam)+' translationRateParamZfast='+str(controlPanel.translationRateParamZfast)+' translationRateParamZslow='+str(controlPanel.translationRateParamZslow)+' gearShiftDistance='+str(controlPanel.gearShiftDistance)+' | Total docking time ='+str(round(loopTotalTime,2))+' seconds \n'
        print('Fail!! translationRateParamXY=',controlPanel.translationRateParamXY,' translationRateParamZ=',controlPanel.translationRateParamZ)
        with open("iss_sim_autopylot_log.txt", "a") as f:
            f.write(writeString)
    browser.close()
    
    plt.plot(rangeTimeList,rangeZList)
    plt.ylabel('Range from ISS (m)')
    plt.xlabel('Time (s))')
    svgName='range_'+time.strftime("%Y%m%d_%H%M%S")+'.svg'
    plt.savefig(svgName)
    plt.draw()
plt.show()