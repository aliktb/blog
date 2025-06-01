#!/usr/bin/env python3

import os
import requests

# Get environment variables
ACCOUNT_ID = os.getenv('ACCOUNT_ID')
CLOUDFLARE_API_KEY = os.getenv('CLOUDFLARE_API_KEY')
PROJECT_NAME = os.getenv('PROJECT_NAME')
URL_TO_DELETE = os.getenv('URL_TO_DELETE')

# Check if env vars are set
if not ACCOUNT_ID:
  print("Error: ACCOUNT_ID is not set.")
  exit(1)
if not CLOUDFLARE_API_KEY:
  print("Error: CLOUDFLARE_API_KEY is not set.")
  exit(1)
if not PROJECT_NAME:
  print("Error: PROJECT_NAME is not set.")
  exit(1)
if not URL_TO_DELETE:
  print("Error: URL_TO_DELETE is not set.")
  exit(1)


# Get deployment ID to delete
api_url=f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/pages/projects/{PROJECT_NAME}/deployments"

# Setup headers
headers = {
  "Authorization": f"Bearer {CLOUDFLARE_API_KEY}"
}

response = requests.get(api_url, headers=headers)

print("Response from API:")
# print(response.json())  # Assuming the response is in JSON format

# Get IDs where alias URL is either URL_TO_DELETE or null
# The alias is set to null if has been overwritten. i.e. the alias URL now
# belongs to superseding deployment

list_of_deployment_ids_to_delete=[]

response_as_json = response.json()

results = response_as_json['result']

for result in results:
  aliases = result['aliases']
  deployment_id = result['id']
  if(aliases == None):
    print(f'Alias is None. ID is {deployment_id}')
    list_of_deployment_ids_to_delete.append(deployment_id)
  elif(URL_TO_DELETE in aliases):
    print(f'{URL_TO_DELETE} is in aliases. ID is {deployment_id}')
    list_of_deployment_ids_to_delete.append(deployment_id)
  else:
    print(f'{deployment_id} is not None or does not include {URL_TO_DELETE}. Not deleting')

print(f'List of deployment IDs to delete is {list_of_deployment_ids_to_delete}')

for deployment_id in list_of_deployment_ids_to_delete:
  print(f'Deleting {deployment_id}')

  # NOTE: You cannot delete an aliased deployment without a `?force=true` parameter in the API request URL.
  delete_api_url=f'https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/pages/projects/{PROJECT_NAME}/deployments/{deployment_id}?force=true'

  requests.delete(delete_api_url, headers=headers)

  print(f'{deployment_id} deleted')
