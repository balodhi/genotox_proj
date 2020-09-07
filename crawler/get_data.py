import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotVisibleException, StaleElementReferenceException
import platform
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os.path as osp

class get_data:
  def __init__(self):
    executable = ''
    if platform.system() == 'Windows':
        print('Detected OS : Windows')
        executable = './chromedriver/chromedriver_win.exe'
    elif platform.system() == 'Linux':
        print('Detected OS : Linux')
        executable = './chromedriver/chromedriver_linux'
    elif platform.system() == 'Darwin':
        print('Detected OS : Mac')
        executable = './chromedriver/chromedriver_mac'
    else:
        raise OSError('Unknown OS Type')
    
    if not osp.exists(executable):
        raise FileNotFoundError('Chromedriver file should be placed at {}'.format(executable))

    self.browser = webdriver.Chrome(executable)
    
    browser_version = 'Failed to detect version'
    chromedriver_version = 'Failed to detect version'
    major_version_different = False

    if 'browserVersion' in self.browser.capabilities:
        browser_version = str(self.browser.capabilities['browserVersion'])

    if 'chrome' in self.browser.capabilities:
        if 'chromedriverVersion' in self.browser.capabilities['chrome']:
            chromedriver_version = str(self.browser.capabilities['chrome']['chromedriverVersion']).split(' ')[0]

    if browser_version.split('.')[0] != chromedriver_version.split('.')[0]:
        major_version_different = True
    
    print('_________________________________')
    print('Current web-browser version:\t{}'.format(browser_version))
    print('Current chrome-driver version:\t{}'.format(chromedriver_version))
    if major_version_different:
        print('warning: Version different')
        print('Download correct version at "http://chromedriver.chromium.org/downloads" and place in "./chromedriver"')
    print('_________________________________')
    
  def get_scroll(self):
    pos = self.browser.execute_script("return window.pageYOffset;")
    return pos

  def wait_and_click(self, xpath):
    #  Sometimes click fails unreasonably. So tries to click at all cost.
    try:
        w = WebDriverWait(self.browser, 15)
        elem = w.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        elem.click()
    except Exception as e:
        print('Click time out - {}'.format(xpath))
        print('Refreshing browser...')
        self.browser.refresh()
        time.sleep(2)
        return self.wait_and_click(xpath)

    return elem
  
  def echa(self, url):
  	self.browser.get(url)
  	
  	html = driver.page_source
  	
  	if html.contains("404 not found"):
  		return page_not_found
  	
  	return html
  	
  	
  	
  
if __name__ == '__main__':
  collect = get_data()
  links = collect.naver_full('박보영')
  print(len(links), links)