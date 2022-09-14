import argparse
from asyncio.log import logger
import csv
import json
import requests
from requests.auth import HTTPBasicAuth
import logger

log = logger.get_logger("jirafunctions")


#function to read command line arguments and parse them
def argparser():
    parser = argparse.ArgumentParser(description='Jira automation')
    parser.add_argument('--csv1', type=str, required=True)
    parser.add_argument('--csv2', type=str, required=True)
    parser.add_argument('--domain_name', type=str, required=True)
    parser.add_argument('--email', type=str, required=True)
    parser.add_argument('--api_t', type=str, required=True)

    arg = parser.parse_args()

    return arg
#function to create a feature and returns the feature key
def create_feature(domain_name, email, api_t, issuetype, featurename, summary, description, assignee, labels, reporterID, key, priority):
    url = "https://{}.atlassian.net/rest/api/3/issue".format(domain_name)

    auth = HTTPBasicAuth('{}'.format(email),'{}'.format(api_t))

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    data = {}
    data['fields']={}
    fields = data['fields']
    fields['project'] = {'key': key}
    fields['summary'] = summary
    fields['issuetype'] = {'name': issuetype}
    fields['components'] = [{}]
    fields['reporter'] = {'accountId': reporterID}
    fields['labels'] = [labels]
    fields['priority'] = {'id': priority}
    fields['assignee'] = assignee
    fields['customfield_10011'] = featurename
    #fields['customfield_10014'] = featurekey   #key to link to feature
    fields['description'] = {'type':'doc', 'version':1, 'content':[{'type': 'paragraph', 'content':[{'text':description, 'type':'text'}]}]}
    
    payload = json.dumps(data)
    #log.debug(json.dumps(jdata, indent = 2))
    response = requests.request("POST", url, data=payload, headers=headers,auth=auth )

    #log.debug(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
    log.debug(response.text)
    feature = json.loads(response.text)

    return feature['key']

#function to create story templates under each feature
def create_story(domain_name, email, api_t, issuetype, projectkey, reporterID, labels, priority, assignee, featurelink, summary,description):
    url = "https://{}.atlassian.net/rest/api/3/issue".format(domain_name)

    auth = HTTPBasicAuth('{}'.format(email),'{}'.format(api_t))

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    data = {}
    data['fields']={}
    fields = data['fields']
    fields['project'] = {'key': projectkey}
    fields['summary'] = summary
    fields['issuetype'] = {'name': issuetype}
    fields['components'] = [{}]
    fields['reporter'] = {'accountId': reporterID}
    fields['labels'] = [labels]
    fields['priority'] = {'id': priority}
    fields['assignee'] = assignee
    #fields['customfield_10011'] = featurename
    fields['customfield_10014'] = featurelink   #featurekey to link to feature
    fields['description'] = {'type':'doc', 'version':1, 'content':[{'type': 'paragraph', 'content':[{'text':description, 'type':'text'}]}]}
   
    
    
    payload = json.dumps(data)
    #log.debug(json.dumps(jdata, indent = 2))
    response = requests.request("POST", url, data=payload, headers=headers,auth=auth )

    #log.debug(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
    log.debug(response.text)




