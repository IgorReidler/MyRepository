from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By



chromedriver = "E:\\Python\\chromedriver.exe"
browser=webdriver.Chrome(chromedriver)
#browser.get("http://www.learningaboutelectronics.com/Articles/How-to-click-a-button-with-Javascript.php")
browser.get("https://iss-sim.spacex.com/")

#wait
wait = WebDriverWait(browser, 100)
#elem = wait.until(EC.element_to_be_clickable((By.ID, 'begin-button')))
#print(elem.text)
#elem.click()
#wait until up is clickable
elem = wait.until(EC.element_to_be_clickable((By.ID, 'translate-up-button')))
print('up-button clickable!!!')

#Rotation Error
rollError = browser.find_element_by_xpath("//div[@id='roll']/div[@class='error']")
pitchError = browser.find_element_by_xpath("//div[@id='pitch']/div[@class='error']")
yawError = browser.find_element_by_xpath("//div[@id='yaw']/div[@class='error']")
#Translation Error
xError = browser.find_element_by_xpath("//div[@id='x-range']/div[@class='distance']")
yError = browser.find_element_by_xpath("//div[@id='y-range']/div[@class='distance']")
zError = browser.find_element_by_xpath("//div[@id='z-range']/div[@class='distance']")
range = browser.find_element_by_xpath("//div[@id='range']/div[@class='rate']")
#Rotation Rates
rollRate = browser.find_element_by_xpath("//div[@id='roll']/div[@class='rate']")
pitchRate = browser.find_element_by_xpath("//div[@id='pitch']/div[@class='rate']")
yawRate = browser.find_element_by_xpath("//div[@id='yaw']/div[@class='rate']")
#Translation Rates
#xRate = browser.find_element_by_xpath("//div[@id='x-range']/div[@class='distance']")
#yRate = browser.find_element_by_xpath("//div[@id='y-range']/div[@class='distance']")
#zRate = browser.find_element_by_xpath("//div[@id='z-range']/div[@class='distance']")
rangeRate = browser.find_element_by_xpath("//div[@id='rate']/div[@class='rate']")



#printing current R/T
print('rollError =',rollError.text)
print('pitchError =',pitchError.text)
print('yawError =',yawError.text)

print('xError =',xError.text)
print('yError =',yError.text)
print('zError =',zError.text)
print('rangeError =',range.text)

print('rollRate =',rollRate.text)
print('pitchError =',pitchRate.text)
print('yawError =',yawRate.text)

#print('xRate =',xRate.text)
#print('yRate =',yRate.text)
#print('zRate =',zRate.text)
print('rangeRate =',rangeRate.text)

#Actions
upButton=browser.find_element_by_id('translate-up-button')
upButton.click()
downButton=browser.find_element_by_id('translate-down-button')
downButton.click()


#stuff that work but are not needed
#rollId=browser.find_elements_by_id('roll')
#rollError=rollId.find_element_by_class_name('error')