from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from pyvirtualdisplay import Display
import time
from selenium.webdriver.common.by import By

''' for Ubuntu SERVER '''
# cap = DesiredCapabilities().FIREFOX
# display = Display(visible=0, size=(600, 400)).start()
# driver = webdriver.Firefox(capabilities=cap, executable_path='/home/ubuntu/anaconda3/bin/geckodriver')

''' for Window Client '''
driver = webdriver.Firefox()

urlMain = "https://www.freitag.ch/en/shop/bags"

driver.get(urlMain)
time.sleep(1)
elemfilter = driver.find_elements(By.CLASS_NAME ,'store-products-list')
urlModel = []

for i in elemfilter:
    elemUrl = i.find_elements(By.TAG_NAME,'h3')

    for j in elemUrl:
        pureUrl = j.find_element(By.TAG_NAME,'a')
        url = pureUrl.get_attribute('href')
        url = url.split('?')[0]
        # print(url)
        urlModel.append(url)
        
# print(urlModel)

for k in urlModel:
    driver.get(k)
    driver.find_element(By.ID,'products-load-all').click()
    productList = driver.find_elements(By.CLASS_NAME,'products-list')

    for l in productList:
        print(l.text)
    
    break

print('All Done')

driver.close()    
