import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import numpy as np
import pydeck as pdk
import streamlit as st
import requests


usernameLinkedIn=st.text_input('Email adress', 'tartampion@lesgoudes.om')
passwordLinkedIn =  st.text_input('Password', 'scalability123$')
uploaded_file = st.file_uploader("Import your csv")
count=0
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    options = webdriver.FirefoxOptions()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Remote(
        command_executor='http://165.227.169.86:4444/wd/hub',
        options = options
    )
    driver.get("https://www.linkedin.com/uas/login")
    df = df.head(20)
    login = driver.find_element(By.XPATH,"/html/body/div/main/div[3]/div[1]/form/div[1]/input").send_keys(usernameLinkedIn)
    password = driver.find_element(By.XPATH,"/html/body/div/main/div[3]/div[1]/form/div[2]/input").send_keys(passwordLinkedIn)
    login = driver.find_element(By.XPATH,"/html/body/div/main/div[3]/div[1]/form/div[3]/button").click()
    #driver.get(df['profile_url'][0])
    #driver.get(df['profile_url'][0])
    urls = []
    url_converted=[]
    count=0
    for i in df['linkedin_url']:
        driver.get('http://'+i)
        urls.append('http://'+i)
        time.sleep(3)
        url_converted.append(driver.current_url)
        count+=1
        if count%5==0:
            driver.quit()
            time.sleep(10)
            options = webdriver.FirefoxOptions()
            options.add_argument('--ignore-ssl-errors=yes')
            options.add_argument('--ignore-certificate-errors')
            driver = webdriver.Remote(
                command_executor='http://165.227.169.86:4444/wd/hub',
                options = options
            )
            driver.get("https://www.linkedin.com/uas/login")
            login = driver.find_element(By.XPATH,"/html/body/div/main/div[3]/div[1]/form/div[1]/input").send_keys(usernameLinkedIn)
            password = driver.find_element(By.XPATH,"/html/body/div/main/div[3]/div[1]/form/div[2]/input").send_keys(passwordLinkedIn)
            submit = driver.find_element(By.XPATH,"/html/body/div/main/div[3]/div[1]/form/div[3]/button").click()
            print('On a converti '+str(count)+' urls')
    df_final = pd.DataFrame(urls)
    df_final['url_converted']=url_converted
    st.write(df_final)

