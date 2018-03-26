from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from pyvirtualdisplay import Display
from elasticsearch import Elasticsearch
from linebot import LineBotApi
from linebot.models import TextSendMessage,ImageCarouselColumn,URITemplateAction,TemplateSendMessage,ImageCarouselTemplate
from linebot.exceptions import LineBotApiError
import time

''' for Ubuntu SERVER '''
cap = DesiredCapabilities().FIREFOX
display = Display(visible=0, size=(600, 400)).start()
driver = webdriver.Firefox(capabilities=cap, executable_path='/home/ubuntu/anaconda3/bin/geckodriver')

''' for Window Client '''
# driver = webdriver.Firefox()

line_bot_api = LineBotApi('fSDjokoamI2lnlDZE8GJ2+PoZBn8DHsDba8zCtW57zR++3X+Iiy5jwtMQFB1oynrcHd3pU4g5S3IikMXzTmCkPueLieW/ilvst42POA6I6cyt/+z3u13OPxjof+Jq12l046ITxA2+sSMC95uRwEdHQdB04t89/1O/w1cDnyilFU=')
es = Elasticsearch('https://search-test-bot-esek4kvzcdw2qmdhyqqhpi2ldq.ap-southeast-1.es.amazonaws.com')
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
        urlModel.append(url)

urlRemove = [
    'https://www.freitag.ch/en/e002',
    'https://www.freitag.ch/en/e001',
    'https://www.freitag.ch/en/r121',
    ]
urlModel = [x for x in urlModel if x not in urlRemove]

# ## config for test
# urlModel = urlModel[0:1]

urlModel = list(set(urlModel))
print(len(urlModel))

# exit()

newProduct = []

for k in urlModel:
    print(urlModel.index(k))
    driver.get(k)
    time.sleep(1)
    try:
        driver.find_element(By.ID,'products-load-all').click()
        time.sleep(10)
    except:
        pass
    
    try:
        namemodel = driver.find_element(By.CLASS_NAME,'title').text.split('\n')[0]
        allProduct = driver.find_element(By.CLASS_NAME,'products-list')
        product = allProduct.find_elements(By.TAG_NAME,'a')
        m = 1
        for l in product:
            
            productUrl = l.get_attribute('href')
            idProduct = productUrl.split('=')[1]
            imgtag = l.find_element(By.TAG_NAME,'img')
            productImg = imgtag.get_attribute('src')
            # print(m,idProduct,productUrl,productImg)
            m += 1
            
            doc = {
                'url' : productUrl,
                'img' : productImg,
            }
            
            ### Save to Elastic
            res = es.index(index="f-store-index", doc_type='product', id=idProduct, body=doc)
            
            if res['result'] == 'created':
                print('created', idProduct)
                try:
                    product =  ImageCarouselColumn(
                                    image_url = productImg,
                                    action=URITemplateAction(
                                        label=namemodel,
                                        uri= productUrl,
                                    )
                                )
                    
                    newProduct.append(product)
                    if len(newProduct) == 10:
                        ## Sent to Line API
                        image_carousel_template_message = TemplateSendMessage(
                            alt_text='Now Arrival',
                            template=ImageCarouselTemplate(
                                columns= newProduct
                            )
                        )
                        user = ['Ub86505e4cdcf67fb339cc8018aad9306','U9d261d005044ab0f2cba21b69278a155']
                        line_bot_api.multicast(user,image_carousel_template_message)

                        newProduct = []                            

                except LineBotApiError as e:
                    print(e.error)
            else:
                # print('updated')
                pass
            
    except:
        pass


## Sent to Line API
image_carousel_template_message = TemplateSendMessage(
        alt_text='Now Arrival',
        template=ImageCarouselTemplate(
            columns= newProduct
        )
    )
## LINE ID Dell: U9d261d005044ab0f2cba21b69278a155 || Ness : Ub86505e4cdcf67fb339cc8018aad9306
# line_bot_api.push_message('U9d261d005044ab0f2cba21b69278a155', image_carousel_template_message)
user = ['Ub86505e4cdcf67fb339cc8018aad9306','U9d261d005044ab0f2cba21b69278a155']
line_bot_api.multicast(user,image_carousel_template_message)
    

print('All Done')
driver.close()    
