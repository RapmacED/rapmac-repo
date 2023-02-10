from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import pydeck as pdk
import streamlit as s
import json
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import streamlit as st


st.title('Welcome to the Scalability HardForce platform')
st.subheader('Upload the list of the emails to check')
uploaded_file = st.file_uploader("Import your csv")
uploaded_file = None

@st.cache
def process_browser_log_entry(entry):
    response = json.loads(entry['message'])['message']
    return response

@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False,sep=',')

def send(driver, cmd, params={}):
  resource = "/session/%s/chromium/send_command_and_get_result" % driver.session_id
  url = driver.command_executor._url + resource
  body = json.dumps({'cmd': cmd, 'params': params})
  response = driver.command_executor._request('POST', url, body)
  return response.get('value')


def registeredOrNot(events):
    for i in range(len(events)):
        if 'params' in events[i]:
            if 'response' in events[i]['params']:
                if 'url' in events[i]['params']['response']:
                    #print(events[i]['params']['response']['url'])
                    if events[i]['params']['response']['url']=='https://app.blacksales.co/users/password':
                        #print(str(send(driver,'Network.getResponseBody', {'requestId': events[i]["params"]["requestId"]})))
                        if 'Email not found' in str(send(driver,'Network.getResponseBody', {'requestId': events[i]["params"]["requestId"]})):
                            return False
    return True

count = 0
percent_complete = 0
result=[]

if uploaded_file is not None and count ==0:
    df=pd.read_csv(uploaded_file)
    if 'email' not in df:
        st.error("The uploaded file does not have \'email\' colmun", icon="🚨")
        uploaded_file = None
    else:
        per = 1/len(df)
        my_bar = st.progress(0)
        for i in df['email']:
            options = webdriver.ChromeOptions()
            options.add_argument('--ignore-ssl-errors=yes')
            options.add_argument('--ignore-certificate-errors')
            options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
            driver = webdriver.Remote(
                command_executor='http://165.227.169.86:4444/wd/hub',
                options=options
            )
            print('1')
            driver.get('https://app.blacksales.co/users/password/new')
            sleep(3)

            login = driver.find_element(By.XPATH,"/html/body/div[2]/div/div[2]/div/form/div/input").send_keys('rapmac11@gmail.com')
            submit = driver.find_element(By.XPATH,"/html/body/div[2]/div/div[2]/div/form/button").click()
            print('2')
            browser_log = driver.get_log('performance') 
            print('3')
            events = [process_browser_log_entry(entry) for entry in browser_log]
            print('4')
            events = [event for event in events if 'Network.response' in event['method']]

            #if "https://app.blacksales.co/users/password/new" in events[i]['params']['url']:
            #print(i)
            result.append(registeredOrNot(events))
            print(registeredOrNot)
            driver.quit()
            count+=1
            percent_complete+=per
            my_bar.progress(percent_complete)
        df['result']=result
        csv = convert_df(df)

        uploaded_file = None
        st.download_button(
            label="Download the result as CSV",
            data=csv,
            file_name='result_scrap.csv',
            mime='text/csv',
        )


