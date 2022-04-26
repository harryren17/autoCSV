from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import threading
import pyautogui
import string
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

first = '7492e7.PNG'
second = '1e5dlight.png'

PATH = "C:\Program Files (x86)\chromedriver.exe"

def runapp():
    opened = False
    count = 0
    myfile = open("linksfile.txt")
    options = webdriver.ChromeOptions()
    options.add_argument('ignore-certificate-errors')
    driver = webdriver.Chrome(PATH, chrome_options=options)
    for line in myfile:
        if "https" in line:
            if not opened:
                #open the first time (need the certificate thread)
                print(line) 
                openLinkWrapper(driver, line, opened, count)
                opened = True
                count += 1
            else:
                #opening a new tab (does not require the certifiate thread)
                openLinkWrapper(driver, line, opened, count)
                count += 1
    time.sleep(1)
    driver.quit()
            
def certAccept():
    #selects the certificate
    time.sleep(3)
    pyautogui.press('tab')

    (x,y) = list(pyautogui.locateCenterOnScreen(first))

    pyautogui.click(x=x,y=y,clicks=1)
    pyautogui.press('enter')

def openLinkWrapper(driver,link,opened,count):
    
    if not opened:
        #thread the certificate accept function
        acceptCert = threading.Thread(target= certAccept)
        acceptCert.start()
        openLink(driver,link)

    else:
        #open a new tab and repeat the link click code
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[count])
        openLink(driver,link)
        

def openLink(driver,link):
        driver.get(link)
        try:
            table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,"//*[@id='reportTable']" ))
            )
        except:
            print('webpage not found', f'{link}')
        
        table = driver.find_elements_by_xpath("//*[@id='reportTable']")
        
        for i in table:
            lstlin = i.text.splitlines ()
            break
        
        #print line below for debugging links
        #print(lstlin[1])
        if "xml" in lstlin[1]:
            link = driver.find_element_by_xpath("//*[@id='reportTable']/tbody/tr[2]/td[4]/a")
            link.click()
        elif "csv" in lstlin[1]:
            link = driver.find_element_by_xpath("//*[@id='reportTable']/tbody/tr[1]/td[4]/a")
            link.click()
        else:
            link = driver.find_element_by_xpath("//*[@id='reportTable']/tbody/tr[1]/td[4]/a")
            link.click()

        #pause time to download in seconds
        time.sleep(10)

if __name__ == "__main__":
    
    runapp()

