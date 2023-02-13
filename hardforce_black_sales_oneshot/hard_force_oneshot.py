from typing import Dict, Any

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep
import json
import pandas as pd
import airplane

def process_browser_log_entry(entry):
    response = json.loads(entry['message'])['message']
    return response


def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False,sep=',')

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
                            return False
    return True

def main(params: Dict[str, Any]) -> Dict[str, Any]:
    """options = webdriver.ChromeOptions()
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
    login = driver.find_element(By.XPATH,"/html/body/div[2]/div/div[2]/div/form/div/input").send_keys(params['email'])
    submit = driver.find_element(By.XPATH,"/html/body/div[2]/div/div[2]/div/form/button").click()
    print('2')
    browser_log = driver.get_log('performance') 
    print('3')
    events = [process_browser_log_entry(entry) for entry in browser_log]
    print('4')
    events = [event for event in events if 'Network.response' in event['method']]
    #if "https://app.blacksales.co/users/password/new" in events[i]['params']['url']:
    #print(i)
    result = registeredOrNot(events, driver)
    driver.quit()"""
    
    
    df = pd.read_csv('/Users/raph/Documents/Dataship_Code/lW4B.csv')
    df.head()
    table = {'email': df['company_industry'],
             'result': df['company_name']}
    rows = []

    for i in range(len(df)):
        row = {'email': df['company_industry'][i],
             'result': df['company_name'][i]}
        rows.append(row)
    
    airplane.display.table(
        rows
    )

    """if result == False:
        response = params['email'] + ' does not have BlackSales account'
    else:
        response = params['email'] + ' has BlackSales account'
    return response"""
    










