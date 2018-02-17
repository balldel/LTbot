from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
from pyvirtualdisplay import Display

# chromedriver = '/Users/arsadell/Documents/Github/LTbot/'
# os.environ["webdriver.chrome.driver"] = chromedriver
display = Display(visible=0, size=(1920, 1080)).start()
driver = webdriver.Firefox()
urlclean = ["https://www.google.co.th",
            # "http://manager:11946++cmma@202.129.207.202:8080/probe/",
            # "http://manager:11946++cmma@27.254.46.193/:8080/probe/",
            # "http://manager:11946++cmma@202.129.207.215/:8080/probe/",
            # "http://manager:11946++cmma@103.22.182.186//:8080/probe/",
            # "http://manager:11946++cmma@103.13.30.221/:8080/probe/",
        ]
for clean in urlclean:
    driver.get(clean)
    print('Start Clean', clean)
    elem = driver.find_elements_by_xpath("//img[@alt='reload']")
    for i in elem:
        print(i.tag_name)
        i.click()
        print('Cleaned')
print('All Done')
    


# assert "Python" in driver.title
# elem = driver.find_element_by_name("q")
# elem.clear()
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source
# driver.close()
