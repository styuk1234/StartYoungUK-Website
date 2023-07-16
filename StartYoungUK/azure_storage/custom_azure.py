from storages.backends.azure_storage import AzureStorage
import os

conn_str = os.environ['AZURE_CONNECTION_STRING']
conn_str_params = {pair.split('=')[0]: pair.split(
   '=')[1] for pair in conn_str.split(' ')}

print(conn_str_params['AccountName'])

class PublicAzureStorage(AzureStorage):
    account_name = conn_str_params['AccountName']
    account_key = conn_str_params['AccountKey']
    azure_container = 'media'
    expiration_secs = None