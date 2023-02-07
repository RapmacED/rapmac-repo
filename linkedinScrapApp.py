import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import pydeck as pdk
import streamlit as st
from math import floor


st.title('Welcome to Scalability LinkedIn Open Data reader')
uploaded_file = st.file_uploader("Import your csv")
options = webdriver.FirefoxOptions()
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')
@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False,sep=',')
poste = []
count = 0
percent_complete = 0
if uploaded_file is not None and count==0:
    df=pd.read_csv(uploaded_file)
    per = 1/len(df)
    my_bar = st.progress(0)
    for i in df['urls']:
        driver = webdriver.Remote(
            command_executor='http://165.227.169.86:4444/wd/hub',
            options = options
        )
        print(i)
        driver.get(i)
        #poste.append(driver.find_element(By.XPATH,'/html/head/meta[20]'))
        time.sleep(3)
        poste.append(driver.page_source)
        count+=1
        percent_complete+=per
        my_bar.progress(percent_complete)
        #driver.find_element(By.CLASS_NAME,'modal__dismiss btn-tertiary h-[40px] w-[40px] p-0 rounded-full indent-0 contextual-sign-in-modal__modal-dismiss absolute right-0 m-[20px] cursor-pointer').click()
        driver.quit()
    df['poste']=poste
    csv = convert_df(df)
  
    st.download_button(
        label="Download the result as CSV",
        data=csv,
        file_name='result_scrap.csv',
        mime='text/csv',
    )
    st.stop()
    st.success('You can now download your file')