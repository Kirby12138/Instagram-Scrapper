#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random
import csv
import time
import numpy as np
import pandas as pd
from selenium import webdriver
import re


# In[38]:


driver = webdriver.Chrome('/Users/nidachen/Desktop/Crawler/chromedriver')
driver.get("https://www.instagram.com/")


# In[3]:


email = 'NDDDCCC'
password = ''


# In[4]:


xpath_email = "//*[contains(@name, 'username')]"
email_element = driver.find_elements_by_xpath(xpath_email)
email_element[0].clear()
email_element[0].send_keys(email)

time.sleep(0.8)


# In[5]:


xpath_password = "//*[contains(@type, 'password')]"
password_element = driver.find_elements_by_xpath(xpath_password)
password_element[0].clear()
password_element[0].send_keys(password)

time.sleep(1+random.random()*2)


# In[6]:


xpath_conti = "//*[contains(@type, 'submit')]"
conti_element = driver.find_elements_by_xpath(xpath_conti)
conti_element[0].click()

time.sleep(1+random.random())


# In[24]:


# save log info: no
try:
    xpath_conti2 = "//*[contains(@class, 'sqdOP yWX7d    y3zKF     ')]"
    conti_element = driver.find_elements_by_xpath(xpath_conti2)
    conti_element[0].click()
except:
    pass

time.sleep(1+random.random())


# In[12]:


# send notifications: no
try:
    xpath_conti2 = "//*[contains(@class, 'aOOlW   HoLwm ')]"
    conti_element = driver.find_elements_by_xpath(xpath_conti2)
    conti_element[0].click()
except:
    pass


# In[7]:


def scroll_down():
    SCROLL_PAUSE_TIME = 1

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

#         # Calculate new scroll height and compare with last scroll height
#         new_height = driver.execute_script("return document.body.scrollHeight")
#         if new_height == last_height:
#             break
#         last_height = new_height


# In[8]:


def form_url_list(num,user):
    st = time.time()
    url_list = list()
    seen = set()
    driver.get("https://www.instagram.com/"+user)
    ct = time.time()
    refreshPage(ct,st)
    for i in range(num):
        xpath_tests = "//div[@class = 'Nnq7C weEfm']//div[@class='v1Nh3 kIKUG _bz0w']//a"
        tests = driver.find_elements_by_xpath(xpath_tests)
        
        for test in tests:

            cur = test.get_attribute("href")

            if cur not in seen:
                seen.add(cur)
                url_list.append(cur)
        print(len(url_list))
        scroll_down()
        driver.implicitly_wait(5)
        time.sleep(random.uniform(9.0,12.0))
    with open('ins_urllist.csv', 'a', encoding='utf-8') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow([user])
        csv_writer.writerow(url_list)
        

    return url_list


# In[9]:


def getPicture(url,postnum,brand):
    driver.get(url)
    driver.implicitly_wait(5)
    time.sleep(random.uniform(0.0,1.0))
    xpath_img = "//div[@class = 'ltEKP']//div[@class = 'KL4Bh']//img"
    try:
        img = driver.find_element_by_xpath(xpath_img)
        img.screenshot(f"/Users/nidachen/Desktop/Crawler/pics/{brand}'s {postnum+1}th post.png")
    except:
        return


# In[10]:


def getTags(raw_text):
    tags = re.compile(r"#(\w+)")
    tags.findall(raw_text)
    return tags.findall(raw_text)


# In[11]:


def getMentions(raw_text):
    mentions = re.compile(r"@([\w\.]+)")
    mentions.findall(raw_text)
    return mentions.findall(raw_text)


# In[12]:


def refreshPage(ct,st):
    while ct - st > 7:
        print("refreshing page...")
        st = time.time()
        driver.refresh()
        driver.implicitly_wait(5)
        ct = time.time()    


# In[13]:


def getImage():
    xpath_img = "//div[@class = 'ltEKP']//div[@class = 'KL4Bh']//img"
    imgs = driver.find_elements_by_xpath(xpath_img)
        
    pics = len(imgs)
    if pics == 0:
        data.append('video is uncollectable')
    else:
        try:
            data.append(imgs[0].get_attribute("src"))
        except IndexError:
            driver.refresh()
            driver.implicitly_wait(5)
            getImage()


# In[14]:


def getpostdate(i,url_list):
    st = time.time()
    driver.get(url_list[i])
    driver.implicitly_wait(5)
    ct = time.time()
    refreshPage(ct,st)
    xpath_date = "//div[@class = 'eo2As  ']//a[@class = 'c-Yi7']//time[@class = '_1o9PC Nzb55']"
    datetime = driver.find_element_by_xpath(xpath_date).get_attribute('datetime')
    date = int(re.sub('-','',datetime[:10]))
    return date


# In[15]:


def findDate(url_list):
    right = len(url_list) - 1
    left = 0
    date = getpostdate(right,url_list)
    print(date)
    if date > 20190101:

        print("posts not included")
        return

    
    while left <= right:
        mid = (left + right)//2
        date = getpostdate(mid,url_list)
        print(date)
        
        if abs(date - 20190101) <= 5 or date == 20190101:
            return mid
        elif date > 20190101:
            left = mid + 1
        elif date < 20190101:
            right = mid - 1
    return left+1


# In[16]:


columns = ['','Picture','Text','Datetime','Likes','Tags','Mentions']
xpath_list = ['user']


# In[19]:



start = time.time()
user = 'ford'
url_list = form_url_list(11, user)
n = findDate(url_list)
indexdic[user] = n
print(user +': ' + str(n))

end = time.time()

print("Finished!!!")
print("Time used: ", str((end - start)/60) + 'Mins')


# In[ ]:


to_scrape = ['landrover','acura','cadillac','lincoln','jaguar',
             'lexususa','genesis_usa','infinitiusa','alfaromeoofficial','volvocars',
            'ramtrucks','gmc','ford','jeep','chrysler','nissan','chevrolet','toyota',
             'dodgeofficial','buickusa','honda','kia.worldwide','volkswagen',
            'hyundaiusa','mini','mazdausa','fiat','subaru_usa','mitsubishimotorsofficial']


# In[85]:



with open('ins_urllist.csv', 'a', encoding='utf-8') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow([user])


# In[21]:


indexdic = {
    'rollsroycecars': 478,
    'ferrari': 1300,
    'lamborghini':1240,
    'astonmartinlagonda':1346,
    'bentleymotors':866,
    'maserati':845,
    'porsche':1628,
    'bmw':3262,
    'audi':525,
    'mercedesbenz':0,
    'tesla':140,
    'landrover':1243,
    'acura':536,
    'cadillac':143,
    'lincoln':469,
    'jaguar':1126,
    'lexus':786,
    'genesis':794,
    'infiniti':356,
    'alfaromeo':650,
    'volvo':352,
    'ramtrucks':694,
    'gmc':567,
    'ford':128,
    'jeep':1004,
    'chrysler':701,
    'nissan': 0,
    'chevrolet': 255,
    'toyota':1703,
    'dodgeofficial':805,
    'buickusa':517,
    'honda': 622,
    'kia':786,
    'volkswagen':976,
    'hyundaiusa':797,
    'mini':1539,
    'mazdausa': 276,
    'fiat': 305,
    'subaru_usa':1277,
    'mitsubishimotorsofficial':369
}


# In[22]:


urldic = dict()


# In[23]:


brand = ''
with open('ins_urllist.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for i,row in enumerate(reader):
            if i % 2 == 1:
                try:
                    brand = str(row[0])
                except:
                    continue
            if i % 2 ==  0:
                url_list = row
                urldic[brand] = url_list
                
print(urldic['alfaromeo'])      
# print(len(url_list))
# print(url_list[1])
# print(brand)
# num = indexdic[brand]
# print(num)


# In[95]:


import requests
import pprint
headers = {
    "user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
    "cookie": "_T_WM=55041160268; XSRF-TOKEN=d30dab; WEIBOCN_FROM=1110006030; MLOGIN=0; M_WEIBOCN_PARAMS=oid%3D4702468102952255%26luicode%3D20000061%26lfid%3D4702468102952255%26uicode%3D20000061%26fid%3D4702468102952255"
}
res = requests.get('https://www.instagram.com/p/CXgmoVJIPzO/', headers = headers)
pprint.pprint(res.text)


# In[18]:



to_scrape = ['rollsroycecars','ferrari','lamborghini','astonmartinlagonda',
             'bentleymotors','maserati','porsche','bmw','audi','mercedesbenz',
             'tesla','landrover','acura','cadillac','lincoln','jaguar',
             'lexus','genesis','infiniti','alfaromeo','volvo',
            'ramtrucks','gmc','ford','jeep','chrysler','nissan','chevrolet','toyota',
             'dodgeofficial','buickusa','honda','kia','volkswagen',
            'hyundaiusa','mini','mazdausa','fiat','subaru_usa','mitsubishimotorsofficial']

print(len(to_scrape))


# In[19]:


seen = set()


# In[43]:


#nf
for x, brand in enumerate(to_scrape):
    if brand in ['maserati', 'ford','porsche','bentleymotors','rollsroycecars','ferrari','mercedesbenz']:
        continue

    source = f'/Users/nidachen/Desktop/Crawler/insFinal/ins_{brand}_final.csv'
    print(brand)
    try:
        with open(source,'r') as f:
            reader = csv.reader(f)
            cnt = 0
            for i,row in enumerate(reader):

                if cnt == 700:
                    break
                try:
                    row[1]
                except:
                    continue
                if row[1][:4] != 'http':
                    #print(row[1])
                    continue
                else:
                    cnt += 1
                    if cnt <= 670:
                        continue
                    postnum = int(row[0][4:]) - 1
                    if indexdic[brand] - postnum <=10:
                        print(brand, 'finished')
                        break
                    if (brand,postnum) in seen:
                        print('skipped')
                        continue
                    getPicture(urldic[brand][postnum],postnum,brand)
                    seen.add((brand, postnum))
                    #print(urldic[brand][postnum],postnum)

    except FileNotFoundError:
        print("filenotfound:", brand)
        continue
            
            
            


# In[122]:



brand = 'volvocars'
#source = f'/Users/nidachen/Desktop/Crawler/insFinal/ins_{brand}_final.csv'
source = f'/Users/nidachen/Desktop/Crawler/insFinal/ins_volvo_final.csv'
with open(source,'r') as f:
    reader = csv.reader(f)
    cnt = 0
    for i,row in enumerate(reader):
        if cnt == 100:
            break
        try:
            row[1]
        except:
            continue
        if row[1][:4] != 'http':
            #print(row[1])
            continue
        else:
            cnt += 1
#             if cnt < 140:
#                 continue
            postnum = int(row[0][4:]) - 1
#             if indexdic[brand] - postnum <=15:
#                 break
            getPicture(urldic[brand][postnum],postnum,brand)


# In[47]:


import time
start = time.time()

for i in range(num):
    getPicture(url_list[i],i,brand)
    print(f"Collecting {i+1}th post... ")
    print("Time used: ", str(round((time.time()-start)/60, 2)), 'mins')
    
print("Finished!!!")


# In[ ]:


import urllib.request
from PIL import Image
  
urllib.request.urlretrieve(url_list[0],"urltest.png")
  
img = Image.open("gfg.png")
img.show()


# In[23]:


output_file = 'ins_nissan01.csv' 
with open(output_file, 'w', encoding='utf-8') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(columns)


# In[28]:


to_scrape = ['nissan']
num = int(input("Please enter how many posts to collect:"))
import time
start_time = time.time()

for user in to_scrape:
    
    url_list = form_url_list(num//10 if num > 12 else num, user)
    #num = indexdic[user]

    with open(output_file, 'a', encoding='utf-8') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow([user])

    for i in range(num):
        st = time.time()
        
        print(f"Collecting {user}'s {i+1}th post... ")
        print("Time used: ", str(round((time.time()-start_time)/60, 2)), 'mins')
        driver.get(url_list[i])

        driver.implicitly_wait(5)
        post_x = 'post' + str(i+1)
        data = [post_x]

        xpath_img = "//div[@class = 'KL4Bh']//img"
        ct = time.time()
        
        refreshPage(ct,st)  
        getImage()
        
        time.sleep(random.uniform(0.0,1.0))
        xpath_img = "//div[@class = 'ltEKP']//div[@class = 'KL4Bh']//img"
        try:
            img = driver.find_element_by_xpath(xpath_img)
            img.screenshot(f"/Users/nidachen/Desktop/Crawler/pics/{user}'s {i+1}th post.png")
        except:
            continue
        
        xpath_text = "//div[@class = 'C4VMK']"
        try:
            text = driver.find_element_by_xpath(xpath_text)
            sep = text.text.split('\n')
            content = '\n'.join(sep[:-1])
            data.append(content)
        except:
            data.append(' ')

        xpath_date = "//div[@class = 'eo2As  ']//a[@class = 'c-Yi7']//time[@class = '_1o9PC Nzb55']"
        try:
            datetime = driver.find_element_by_xpath(xpath_date).get_attribute('datetime')
            data.append(datetime[:10])
        except:
            refreshPage(ct+8,ct)
        try:
            xpath_like = "//*[contains(@class, 'zV_Nj')]"
            like = driver.find_element_by_xpath(xpath_like)
            data.append(like.text)
        except:
            data.append(' ')
        
        tags = getTags(content)
        if not tags:
            data.append(" ")
        else:
            data.append('\n'.join(tags))
            
        mentions = getMentions(content)
        if not mentions:
            data.append(" ")
        else:
            data.append('\n'.join(mentions))


        with open(output_file, 'a', encoding='utf-8') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(data)


    
print("Finished!!!")


# In[ ]:




