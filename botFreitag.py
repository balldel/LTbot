from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from pyvirtualdisplay import Display
import time
from selenium.webdriver.common.by import By
from elasticsearch import Elasticsearch

''' for Ubuntu SERVER '''
# cap = DesiredCapabilities().FIREFOX
# display = Display(visible=0, size=(600, 400)).start()
# driver = webdriver.Firefox(capabilities=cap, executable_path='/home/ubuntu/anaconda3/bin/geckodriver')

''' for Window Client '''
driver = webdriver.Firefox()

es = Elasticsearch()
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
urlRemove = [
    'https://www.freitag.ch/en/e002',
    'https://www.freitag.ch/en/e001',
    'https://www.freitag.ch/en/r121',
    ]
urlModel = [x for x in urlModel if x not in urlRemove]

print(urlModel)
# exit()
for k in urlModel:
    driver.get(k)
    time.sleep(1)
    try:
        driver.find_element(By.ID,'products-load-all').click()
    except:
        pass
    
    try:
        allProduct = driver.find_element(By.CLASS_NAME,'products-list')
        product = allProduct.find_elements(By.TAG_NAME,'a')
        m = 1
        for l in product:
            
            productUrl = l.get_attribute('href')
            idProduct = productUrl.split('=')[1]
            imgtag = l.find_element(By.TAG_NAME,'img')
            productImg = imgtag.get_attribute('src')
            print(m,idProduct,productUrl,productImg)
            m += 1
            doc = {
                'url' : productUrl,
                'img' : productImg,
            }
            res = es.index(index="f-store-index", doc_type='tweet', id=idProduct, body=doc)
            if res['result'] == 'created':
                print('created')
            else:
                print('updated')
    except:
        pass
    
    

print('All Done')
driver.close()    
