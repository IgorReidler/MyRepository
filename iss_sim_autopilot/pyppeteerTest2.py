from pyppeteer import launch
import asyncio

#url = 'https://iss-sim.spacex.com/'
url = 'http://www.learningaboutelectronics.com/Articles/How-to-click-a-button-with-Javascript.php'

async def main():
    global browser
    browser = await launch(headless=False, executablePath='C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe', userDataDir="E:\\Python\\chrome-dev")
    page = await browser.newPage()
    await page.goto(url)

# My code

    title = await page.title()
    print(title)
    await page.click('#selfclick')
    
    #document.getElementById("content").innerHTML
    
    #content = await page.evaluate('document.body.textContent', force_expr=True) #example of getting content
    #success = await page.evaluate('document.getElementById("selfclick");#pagebutton.click();', force_expr=True) #example of evaluating js
    
    pagebutton = await page.getElementById("selfclick")
    await pagebutton.click()

# end My code    
    await browser.close()

run = asyncio.run(main())