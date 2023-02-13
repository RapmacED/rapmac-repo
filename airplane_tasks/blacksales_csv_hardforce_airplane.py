import airplane
from typing_extensions import Annotated
import io
import csv
import urllib.request
import pandas as pd
import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def process_browser_log_entry(entry):
    response = json.loads(entry['message'])['message']
    return response

def send(driver, cmd, params={}):
  resource = "/session/%s/chromium/send_command_and_get_result" % driver.session_id
  url = driver.command_executor._url + resource
  body = json.dumps({'cmd': cmd, 'params': params})
  response = driver.command_executor._request('POST', url, body)
  return response.get('value')

def registeredOrNot(events, driver):
    for i in range(len(events)):
        if 'params' in events[i]:
            if 'response' in events[i]['params']:
                if 'url' in events[i]['params']['response']:
                    #print(events[i]['params']['response']['url'])
                    if events[i]['params']['response']['url']=='https://app.blacksales.co/users/password':
                        #print(str(send(driver,'Network.getResponseBody', {'requestId': events[i]["params"]["requestId"]})))
                        if 'Email not found' in str(send(driver,'Network.getResponseBody', {'requestId': events[i]["params"]["requestId"]})):
                            return 'False'
    return 'True'

@airplane.task(
    slug="blacksales_csv_hardforce",
    name="BlackSales csv hardforce",
)

def blacksales_csv_hardforce(
    emails_list: Annotated[
        airplane.File,
        airplane.ParamConfig(
            slug="emails_list",
            name="emails_list",
        ),
    ],
):
    result=[]
    #print(emails_list['url'])
    url = emails_list.url
    response = urllib.request.urlopen(url)
    df = pd.read_csv(io.TextIOWrapper(response))
    if 'email' not in df:
        raise Exception(f"email column is not present in input csv file")
    #csv_file = csv.reader(io.TextIOWrapper(response))
    print('1')
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
        result.append(registeredOrNot(events,driver))
        driver.quit()
    df['result']=result
    rows = []
    for i in range(len(df)):
        row = {'email': df['email'][i],
             'result': df['result'][i]}
        rows.append(row)

    airplane.display.table(rows)
    return 'Done'