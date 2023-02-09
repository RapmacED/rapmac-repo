# %%
import requests
import os 
import snowflake.connector
import time
import json
from flask import Flask

# %%

app = Flask(__name__)
@app.route('/')
def index():
    return 'App Works!'

# %%

def getDomain(url):
    url = url.replace("https://www.", "").replace("http://www.", "").replace("www.","")
    return url

def querySFCompany(domain):
    return "select count(*) from dbt_db.models_final.final_companies_flatten where COMPANY_DOMAIN LIKE '" +domain+"'"

def scrappingURL1(domain):
    return "https://app.scrapingbee.com/api/v1/?api_key=MLINMYF4NZMFT3WA37AGIJ54AP10F86H8TDXSFNJSOIG3NRXMKXE04JSEWID422DT3SDOPEHPE2F3VKC&url=http://www."+domain+"&render_js=false&extract_rules={%22links%22:%20{%22selector%22:%20%22//a[contains(@href,%27linkedin.com/company%27)]%22,%20%22type%22:%20%22list%22,%20%22output%22:%20%22@href%22}}"

def scrappingURL2(domain):
    return "https://app.scrapingbee.com/api/v1/?api_key=MLINMYF4NZMFT3WA37AGIJ54AP10F86H8TDXSFNJSOIG3NRXMKXE04JSEWID422DT3SDOPEHPE2F3VKC&url=https%3A%2F%2Fwww.google.com%2Fsearch%3Fq%3Dsite%253Alinkedin.com%252Fcompany%2B"+domain+"&extract_rules=%7B%22first_link%22%3A%7B%22selector%22%3A%22%23search%20a%22%2C%22output%22%3A%22%40href%22%7D%7D&custom_google=True"

def getCaptainDataIntegrations(api_key, project_id):
    url = "https://api.captaindata.co/v3/integrations/linkedin/accounts?page=0"
    api_key = "x-api-key "+api_key
    headers = {
        "Content-Type": "application/json",
        "x-project-id": project_id,
        "Authorization": api_key
    }
    
    response = requests.get(url, headers=headers)
    result= json.loads(response.text)
    print(result)
    uid=[]
    for i in range(len(result['accounts'])):
        if result['accounts'][i]['is_valid'] == True:
            uid.append(result['accounts'][i]['uid'])
    if len(uid)==0:
        raise Exception("Il n\'y a aucun compte LinkedIn valide sur CaptainData")
    return result, uid

def startCaptainDataEndpoint(api_key,project_id, uid, linkedinUrl):
    url = "https://api.captaindata.co/v3/workflows/b7aaec34-6e36-40b3-9f1f-376276d07af1/schedule"
    api_key = "x-api-key "+api_key
    headers = {
        "Content-Type": "application/json",
        "x-project-id": project_id,
        "Authorization": api_key
    }

    body = {
        "steps": [
            {
                "accounts": [
                    uid
                ],
                "parameters": {
                    "extractOpenPositions": False
                },
                "output_column": None,
                "step_uid": "964f6c7c-9c73-4aff-a6e9-790f0c836565"
            }
        ],
        "inputs": [
            {
                "linkedin_company_url": linkedinUrl,
                "url": linkedinUrl
            }
        ],
        "job_name": uid
    }

    response = requests.post(url, headers=headers, data=json.dumps(body))
    result= json.loads(response.text)
    job_uid = result['job_uid']
    return job_uid
# %%

# %%
@app.route('/url=<string:url>/api-key=<string:api_key>/project-id=<string:project_id>/')
def data(url, api_key, project_id):
    query = querySFCompany(getDomain(url))
    DATABASE='dbt_db'
    SCHEMA='models.final'
    ctx = snowflake.connector.connect(
        user='PythonAPI',
        password='ScalabilityPython!2023',
        account='rq37585.eu-west-1',
        warehouse='COMPUTE_WH',
        database=DATABASE,
        schema=SCHEMA
        )
    cs = ctx.cursor()
    cs.execute(query)
    query_id = cs.sfqid
    while ctx.is_still_running(ctx.get_query_status(query_id)):
        time.sleep(1)
    cs.get_results_from_sfqid(query_id)
    results = cs.fetchall()
    print(f'{results[0]}')
    ctx.close()

# %%

    x = requests.get(scrappingURL1(getDomain(url)))
    result = json.loads(x.text)
    print(result)
    print('1')
# %%
    len(result['links'])
    if len(result['links']) != 0:
        linkedinUrl = result['links'][0]
# %%
    elif len(result['links']) == 0:
        result = json.loads(requests.get(scrappingURL2(getDomain(url))).text)
        linkedinUrl = result['first_link']

    print('2')
    """url = "https://api.captaindata.co/v3/integrations/linkedin/accounts?page=0"

    headers = {
        "Content-Type": "application/json",
        "x-project-id": "24dc2e2c-d2e6-433e-81d2-2f87bc87b59d",
        "Authorization": "x-api-key feecb369cafafe86a22255bca8b6293a4c7a2281bd751d453f06693af32f458d"
    }

    response = requests.get(url, headers=headers)
    result= json.loads(response.text)
    print(result)"""

    result = getCaptainDataIntegrations(api_key,project_id)[0]
    uid = getCaptainDataIntegrations(api_key,project_id)[1][0]
    print('3')
    job_uid = startCaptainDataEndpoint(api_key,project_id, uid, linkedinUrl)
    print('4')
    print(job_uid)
    """for i in range(len(result['accounts'])):
        if result['accounts'][i]['is_valid'] == True:

            uid = result['accounts'][i]['uid']
            url = "https://api.captaindata.co/v3/workflows/b7aaec34-6e36-40b3-9f1f-376276d07af1/schedule"

            headers = {
                "Content-Type": "application/json",
                "x-project-id": "24dc2e2c-d2e6-433e-81d2-2f87bc87b59d",
                "Authorization": "x-api-key feecb369cafafe86a22255bca8b6293a4c7a2281bd751d453f06693af32f458d"
            }

            body = {
                "steps": [
                    {
                        "accounts": [
                            uid
                        ],
                        "parameters": {
                            "extractOpenPositions": False
                        },
                        "output_column": None,
                        "step_uid": "964f6c7c-9c73-4aff-a6e9-790f0c836565"
                    }
                ],
                "inputs": [
                    {
                        "linkedin_company_url": linkedinUrl,
                        "url": linkedinUrl
                    }
                ],
                "job_name": uid
            }

            response = requests.post(url, headers=headers, data=json.dumps(body))
            result= json.loads(response.text)
            job_uid = result['job_uid']"""

    url = "https://api.captaindata.co/v3/jobs/"+job_uid+"/results"

    headers = {
        "Content-Type": "application/json",
        "x-project-id": "24dc2e2c-d2e6-433e-81d2-2f87bc87b59d",
        "Authorization": "x-api-key feecb369cafafe86a22255bca8b6293a4c7a2281bd751d453f06693af32f458d"
    }
    response = requests.get(url, headers=headers)
    return response.text
    
    #return 'Aucun compte LinkedIn n\'est actuellement valide sur Captain Data'
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000) 

# %%

