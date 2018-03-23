from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from pyvirtualdisplay import Display
from elasticsearch import Elasticsearch
from linebot import LineBotApi
from linebot.models import TextSendMessage,ImageCarouselColumn,URITemplateAction,TemplateSendMessage,ImageCarouselTemplate
from linebot.exceptions import LineBotApiError
from datetime import datetime as dt
import time

''' for Ubuntu SERVER '''
# cap = DesiredCapabilities().FIREFOX
# display = Display(visible=0, size=(600, 400)).start()
# driver = webdriver.Firefox(capabilities=cap, executable_path='/home/ubuntu/anaconda3/bin/geckodriver')

''' for Window Client '''
driver = webdriver.Firefox()
# profile = webdriver.FirefoxProfile()
# profile.accept_untrusted_certs = True

line_bot_api = LineBotApi('fSDjokoamI2lnlDZE8GJ2+PoZBn8DHsDba8zCtW57zR++3X+Iiy5jwtMQFB1oynrcHd3pU4g5S3IikMXzTmCkPueLieW/ilvst42POA6I6cyt/+z3u13OPxjof+Jq12l046ITxA2+sSMC95uRwEdHQdB04t89/1O/w1cDnyilFU=')
es = Elasticsearch()
urlMain = "https://www.dreamtrips.com"

driver.get(urlMain)
time.sleep(1)

driver.find_element(By.LINK_TEXT,'Log In').click()
driver.find_element(By.ID,'popupusername').send_keys('64349592')
driver.find_element(By.ID,'popuppassword').send_keys('F@123456')
driver.find_element(By.CLASS_NAME ,'loginpopupsubmit').click()
time.sleep(2)
driver.find_element(By.ID,'frm_4_Search').click()
time.sleep(5)

m = 1
newpage = True
while newpage:
    trips = driver.find_elements(By.CLASS_NAME, 'resultsContent')
    for t in trips:
        title = t.find_elements(By.CLASS_NAME, 'wrapper')[0].text
        place = t.find_elements(By.CLASS_NAME, 'wrapper')[1].text
        url = t.find_elements(By.TAG_NAME,'a')[2].get_attribute('href')
        ids = url.split('/')[4]
        dates = t.find_element(By.CLASS_NAME, 'ng-binding').text.split('-')
        startdate = dt.strptime(dates[0].strip() , '%b %d %Y')
        enddate = dt.strptime(dates[1].strip() , '%b %d %Y')
        duration = t.find_element(By.CLASS_NAME, 'results-trip-duration').text.split(' ')[0]
        price = t.find_element(By.CLASS_NAME, 'results-price').find_element(By.TAG_NAME,'b').text.split('$')[1].split('.')[0]
        try:
            discount = t.find_element(By.CLASS_NAME, 'results-apply-points-badge').text
        except:
            discount = 0
        
        doc ={
            'title': title,
            'place' : place,
            'url' : url,
            'startdate' : startdate,
            'enddate' : enddate,
            'duration' : int(duration),
            'price' : float(price),
            'discount' : float(discount)
        }
                
        ### Save to Elastic
<<<<<<< HEAD
        res = es.index(index="test-dreamtrip-index", doc_type='trip', id=ids, body=doc)
=======
        starttime = dt.today()
        res = es.index(index="dreamtrips-index", doc_type='trip', id=ids, body=doc)
>>>>>>> 84759530122e6fc43b70b334f4f1290e6a6b8b8c
        
        if res['result'] == 'created':
            statusdb = 'created'
            
        else:
            statusdb = 'updated'
        endtime = dt.today()
        totaltime = endtime - starttime
        print(m,statusdb,ids,totaltime)
        m += 1
    ### Check new page
    try:
        driver.find_element(By.CLASS_NAME,'fa-caret-right').click()
        time.sleep(3)
    except:
        newpage = False
        
### Sent to Line API
# image_carousel_template_message = TemplateSendMessage(
#         alt_text='Now Arrival',
#         template=ImageCarouselTemplate(
#             columns= newProduct
#         )
#     )
# # line_bot_api.push_message('U9d261d005044ab0f2cba21b69278a155', image_carousel_template_message)
# user = ['Ub86505e4cdcf67fb339cc8018aad9306','U9d261d005044ab0f2cba21b69278a155']
# line_bot_api.multicast(user,image_carousel_template_message)
    
print('All Done')
driver.close()    
