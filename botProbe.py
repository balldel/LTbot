from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from pyvirtualdisplay import Display
from linebot import LineBotApi
from linebot.models import TextSendMessage
import time

''' for Ubuntu SERVER '''
cap = DesiredCapabilities().FIREFOX
display = Display(visible=0, size=(600, 400)).start()
driver = webdriver.Firefox(capabilities=cap, executable_path='/home/ubuntu/anaconda3/bin/geckodriver')

''' for Window & MAC Client '''
# driver = webdriver.Firefox()

line_bot_api = LineBotApi('fSDjokoamI2lnlDZE8GJ2+PoZBn8DHsDba8zCtW57zR++3X+Iiy5jwtMQFB1oynrcHd3pU4g5S3IikMXzTmCkPueLieW/ilvst42POA6I6cyt/+z3u13OPxjof+Jq12l046ITxA2+sSMC95uRwEdHQdB04t89/1O/w1cDnyilFU=')
urlclean = [
            {'site' : 'http://manager:11946++cmma@202.129.207.202:8080/probe/' , 'name' : 'lion'},
            {'site' : 'http://manager:11946++cmma@27.254.46.193:8080/probe/' , 'name' : '4646_1'},
            {'site' : 'http://manager:11946++cmma@202.129.207.215:8080/probe/' , 'name' : '4646_2'},
            {'site' : 'http://manager:11946++cmma@103.22.182.186:8080/probe/' , 'name' : '4646_3'},
            {'site' : 'http://manager:11946++cmma@103.13.30.221:8080/probe/' , 'name' : 'bbk89'},
            {'site' : 'http://manager:11946++cmma@bbk89.info:8080/probe/' , 'name' : 'newlotto'},
        ]
linetext = ''
for clean in urlclean:
    try:
        driver.get(clean['site'])
        time.sleep(1)
        print('Start Clean', clean['name'])
        elem = driver.find_elements_by_xpath("//img[@alt='reload']")
        for i in elem:
            # print(i.tag_name)
            i.click()
            # print('Cleaned')
        linetext = linetext + clean['name'] + ': Clear!!\n'
    except:
        print('Cant Access')
        linetext = linetext + clean['name'] + ': ERROR!!\n'

line_bot_api.push_message('U9d261d005044ab0f2cba21b69278a155', TextSendMessage(text=linetext))

print('All Done')
driver.close()    
