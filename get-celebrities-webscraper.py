from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time
import requests
import os

def persist_image(url, name, targetFolder):
    try:
        image_content = requests.get(url).content
        #print(image_content)
    except Exception as e:
        print(f"ERROR {e} - Could not download {name}")

    try:
        f = open(os.path.join(targetFolder, f"{name}.jpg"), 'wb')
        f.write(image_content)
        f.close()
        print(f"SUCCESS - saved {name}")
    except Exception as e:
        print(f"ERROR {e} - Could not save {name}")

PATH = "C:\Program Files (x86)\chromedriver.exe"
options = Options()
driver = webdriver.Chrome(service=Service(PATH),options=options)
driver.implicitly_wait(3) 

url = 'https://www.imdb.com/search/name/?match_all=true&ref_=nv_cel_m'
driver.get(url)
time.sleep(5)
#for page in range(10):
profileLinks = []
for page in range(20):
    clickableImages = driver.find_elements(By.CLASS_NAME, 'lister-item-image')
    for clickableImage in clickableImages:
        link = clickableImage.find_element(By.TAG_NAME, 'a').get_attribute('href')
        profileLinks.append(link)
    nextPageButton = driver.find_element(By.CLASS_NAME, 'next-page')
    nextPageButton.click()
    time.sleep(10)
for profile in profileLinks:
    try:
        driver.get(profile)
        actorName = driver.find_element(By.XPATH, '/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div/h1/span').text
        print(actorName)
        driver.find_element(By.XPATH, "/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[3]/div[1]/div[1]/div/a").click()
        image = driver.find_element(By.XPATH, "//img[contains(@data-image-id,'curr')]")
        imageURL = image.get_attribute('src')
        persist_image(imageURL, actorName, "scraped-images")
    except Exception as e:
        continue
driver.quit()    
#nextPage = driver.find_element(By.CLASS_NAME, 'next-page')
#nextPage.click()


