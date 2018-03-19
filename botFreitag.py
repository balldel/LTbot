from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from pyvirtualdisplay import Display
from selenium.webdriver.common.by import By
from elasticsearch import Elasticsearch
from linebot import LineBotApi
from linebot.models import TextSendMessage,ImageCarouselColumn,URITemplateAction,TemplateSendMessage,ImageCarouselTemplate
from linebot.exceptions import LineBotApiError
import time

''' for Ubuntu SERVER '''
# cap = DesiredCapabilities().FIREFOX
# display = Display(visible=0, size=(600, 400)).start()
# driver = webdriver.Firefox(capabilities=cap, executable_path='/home/ubuntu/anaconda3/bin/geckodriver')

''' for Window Client '''
driver = webdriver.Firefox()
profile = webdriver.FirefoxProfile()
profile.accept_untrusted_certs = True

line_bot_api = LineBotApi('fSDjokoamI2lnlDZE8GJ2+PoZBn8DHsDba8zCtW57zR++3X+Iiy5jwtMQFB1oynrcHd3pU4g5S3IikMXzTmCkPueLieW/ilvst42POA6I6cyt/+z3u13OPxjof+Jq12l046ITxA2+sSMC95uRwEdHQdB04t89/1O/w1cDnyilFU=')
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

            newProduct = []
            ### Save to Elastic
            res = es.index(index="f-store-index", doc_type='tweet', id=idProduct, body=doc)
            ### Sent to Line API
            if res['result'] == 'created':
                print('created', idProduct)
                try:
                    product =  ImageCarouselColumn(
                                    image_url = productImg,
                                    action=URITemplateAction(
                                        label='F-Finder',
                                        uri= productUrl,
                                    )
                                )
                    
                    newProduct.append(product)
                    
                except LineBotApiError as e:
                    print(e.error)
            else:
                print('updated')

        image_carousel_template_message = TemplateSendMessage(
                alt_text='Freitag',
                template=ImageCarouselTemplate(
                    columns= newProduct
                )
            )
        line_bot_api.push_message('U9d261d005044ab0f2cba21b69278a155', image_carousel_template_message)
            
    except:
        pass

    

print('All Done')
driver.close()    
