from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from pyvirtualdisplay import Display
import time

''' for Ubuntu SERVER '''
# cap = DesiredCapabilities().FIREFOX
# display = Display(visible=0, size=(600, 400)).start()
# driver = webdriver.Firefox(capabilities=cap, executable_path='/home/ubuntu/anaconda3/bin/geckodriver')

''' for Window & MAC Client '''
driver = webdriver.Firefox()

urlclean = [
            "http://manager:11946++cmma@202.129.207.202:8080/probe/",
            "http://manager:11946++cmma@202.129.207.215:8080/probe/",
            "http://manager:11946++cmma@103.22.182.186:8080/probe/",
            "http://manager:11946++cmma@103.13.30.221:8080/probe/",
            "http://manager:11946++cmma@27.254.46.193:8080/probe/",
        ]
for clean in urlclean:
    driver.get(clean)
    time.sleep(1)
    print('Start Clean', clean)
    elem = driver.find_elements_by_xpath("//img[@alt='reload']")
    for i in elem:
        print(i.tag_name)
        i.click()
        print('Cleaned')

print('All Done')
driver.close()    
