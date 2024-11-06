import requests
import json


def define_json_data(terms, params):
    # define the json data to be sent to the API
    json_data = {}
    for i, term in enumerate(terms):
        json_data[term] = params[i]
    
    # if there are no terms, add only_ids to the json_data
    if not json_data:
        json_data['only_ids'] = 'true'
    return json_data

def run(api_key, vaultID, terms = [], params = []):
    
    base_url = f'https://app.collaborativedrug.com/api/v1/vaults/{vaultID}/'
    headers = {'X-CDD-Token': api_key}
    url = base_url + 'molecules'
    
    # combine terms and params into a single dictionary
    json_data = define_json_data(terms, params)
    
    
    response = requests.get(url, headers=headers, data=json_data)
    print(response.json())
    
if __name__ == '__main__':
    # define the API key
    api = 'NDMzM3xmTkFvQXE5NjVPaHBTL0VHRmlLRVJjYStYKzhHTUpmK0RkMm5mc3pYRnVCb1lTbyswdz09'
    vaultID = 7864
    # no terms or params
    run(api, vaultID)