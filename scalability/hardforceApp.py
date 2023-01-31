from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import numpy as np
import pydeck as pdk
import streamlit as st


options = webdriver.ChromeOptions()
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')
driver = webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',
    options = options
)
sleep(5)
st.title('Scalability Hard Force platform')


#Zelty
def check_exists_by_xpath(xpath):
    try:
        driver.find_element(By.XPATH,xpath)
    except NoSuchElementException:
        return False
    return True
emailZelty = st.text_input('Email adress', 'tartampion@lesgoudes.om')
launchZelty = st.button('Test this adress on Zelty')
zeltyState = ""
if(launchZelty == True):
    #driver.get('https://google.com')
    driver.get("https://bo.zelty.fr/mot-de-passe-oublie")
    sleep(5)
    login = driver.find_element(By.XPATH,"/html/body/div/form/div[1]/input").send_keys(emailZelty)
    sleep(2)
    #password = driver.find_element(By.XPATH,"//*[@id="loginform"]/form/div[1]/input").send_keys("password")
    #sleep(2)
    submit = driver.find_element(By.XPATH,"/html/body/div/form/div[2]/input").click()
    if(check_exists_by_xpath("/html/body/div/p[1]") == True):
        if(driver.find_element(By.XPATH,"/html/body/div/p[1]").text == "Cette adresse email n'existe pas dans notre système."):
            zeltyState = 'Cette adresse n\'est pas reliée à Zelty'

st.title(zeltyState)

driver.close()
driver.quit()