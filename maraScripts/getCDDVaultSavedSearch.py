import requests
import pandas as pd
from datetime import date

def run(api_key:str, vault_name:str, project_name:str, search_name:str):
  def get_CDD_id(api_key:str, query:str, query_type:str, vault_id:str):
      headers = {'X-CDD-token':api_key}
  
      base_url = "https://app.collaborativedrug.com/api/v1/vaults"
      
      if query_type == 'vaults':
          id_list = requests.request("GET", base_url, headers=headers)
          id_list_df = pd.DataFrame(id_list.json())
          query_id = id_list_df[id_list_df['name'] == query]['id'].iloc[0]
      else:
          url = base_url + f'/{vault_id}/{query_type}'
          id_list = requests.request("GET", url, headers=headers)
          id_list_df = pd.DataFrame(id_list.json())
          query_id = id_list_df[id_list_df['name'] == query]['id'].iloc[0]
  
      return str(query_id)
      
  def get_CDD_search(api_key:str, vault_id:str, project_id:str, search_id:str, search:str, format:str):
      today = date.today()
      time = today.strftime("%d%m%Y")
      
      headers = {'X-CDD-token':api_key}
  
      url = f'https://app.collaborativedrug.com/api/v1/vaults/{vault_id}/searches/{search_id}?projects={project_id}&format={format}'
  
      search_prep_out = requests.request("GET", url, headers=headers)
      export_id = search_prep_out.json()['id']
  
      url = f'https://app.collaborativedrug.com/api/v1/vaults/{vault_id}/export_progress/{export_id}'
  
      done = False
      while done == False:
          export_status = requests.request("GET", url, headers=headers).json()["status"]
          if "finished" in export_status or "downloaded" in export_status:
              done = True
  
      url = f'https://app.collaborativedrug.com/api/v1/vaults/{vault_id}/exports/{export_id}'
  
      response = requests.request("GET", url, headers=headers)
  
      filename = f'{time}_{search}.csv'
  
      with open(filename, 'wb') as file:
          file.write(response.content)
  
      return None
  
  ###Get Vault ID
  vault_id = get_CDD_id(api_key, vault_name, 'vaults', 'none')
  
  ###Get Project ID
  project_id = get_CDD_id(api_key, project_name, 'projects', vault_id)
  
  ###Get Search ID
  search_name_str = str(search_name)
  search_id = get_CDD_id(api_key, search_name, 'searches', vault_id)
  
  ###Get Saved Search CSV
  get_CDD_search = get_CDD_search(api_key, vault_id, project_id, search_id, search_name, 'csv')
  
  today = date.today()
  time = today.strftime("%d%m%Y")
  
  return print(f"File '{time}_{search_name}.csv' downloaded successfully.")

if __name__ == '__main__':
    api_key = 'NDMzM3xmTkFvQXE5NjVPaHBTL0VHRmlLRVJjYStYKzhHTUpmK0RkMm5mc3pYRnVCb1lTbyswdz09'
    vault_name = 'AtelierTx Real'
    project_name = 'Cavendish Chemistry'
    search_name = 'Synthesized Compounds'
    run(api_key, vault_name, project_name, search_name)