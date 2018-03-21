
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


# In[2]:


driver = webdriver.Firefox()


# In[3]:


urlMain = "https://www.dreamtrips.com"
driver.get(urlMain)


# In[4]:


driver.find_element(By.LINK_TEXT,'Log In').click()


# In[5]:


driver.find_element(By.ID,'popupusername').send_keys('64349592')


# In[6]:


driver.find_element(By.ID,'popuppassword').send_keys('F@123456')


# In[7]:


driver.find_element(By.CLASS_NAME ,'loginpopupsubmit').click()


# In[9]:


driver.find_element(By.ID,'frm_4_Search').click()


# In[12]:


trips = driver.find_elements(By.CLASS_NAME, 'resultsContent')


# In[15]:


t = trips[0]


# In[22]:


title = t.find_elements(By.CLASS_NAME, 'wrapper')[0].text


# In[23]:


place = t.find_elements(By.CLASS_NAME, 'wrapper')[1].text


# In[46]:


dates = t.find_element(By.CLASS_NAME, 'ng-binding').text.split('-')
startdate = dates[0]
enddate = dates[1]


# In[29]:


duration = t.find_element(By.CLASS_NAME, 'results-trip-duration').text.split(' ')[0]


# In[44]:


price = t.find_element(By.CLASS_NAME, 'results-price').find_element(By.TAG_NAME,'b').text.split('$')[1].split('.')[0]


# In[42]:


discount = t.find_element(By.CLASS_NAME, 'results-apply-points-badge').text


# In[49]:


driver.find_element(By.CLASS_NAME,'fa-caret-right').click()

