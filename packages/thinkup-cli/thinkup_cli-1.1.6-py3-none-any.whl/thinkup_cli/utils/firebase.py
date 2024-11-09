import argparse
import requests
import io

from oauth2client.service_account import ServiceAccountCredentials

from thinkup_cli.utils.ui import UI

PROJECT_ID = 'remote-localize'
BASE_URL = 'https://firebaseremoteconfig.googleapis.com'
REMOTE_CONFIG_ENDPOINT = 'v1/projects/' + PROJECT_ID + '/remoteConfig'
REMOTE_CONFIG_URL = BASE_URL + '/' + REMOTE_CONFIG_ENDPOINT
SCOPES = ['https://www.googleapis.com/auth/firebase.remoteconfig']

def get_access_token():
  """Retrieve a valid access token that can be used to authorize requests.

  :return: Access token.
  """
  credentials = ServiceAccountCredentials.from_json_keyfile_name(
      'service-account-credentials.json', SCOPES)
  access_token_info = credentials.get_access_token()
  return access_token_info.access_token

def publish(etag):
  with open('config.json', 'r', encoding='utf-8') as f:
    content = f.read()
  headers = {
    'Authorization': 'Bearer ' + get_access_token(),
    'Content-Type': 'application/json; UTF-8',
    'If-Match': etag
  }
  resp = requests.put(REMOTE_CONFIG_URL, data=content.encode('utf-8'), headers=headers)
  if resp.status_code == 200:
    UI().psuccess(f'Template published successfully, Etag: {resp.headers['ETag']}')
  else:
    UI().perror(f'Unable to publish template: {resp.text}')