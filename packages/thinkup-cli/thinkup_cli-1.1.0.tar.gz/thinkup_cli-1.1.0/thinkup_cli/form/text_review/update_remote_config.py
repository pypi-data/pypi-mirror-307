import io
import requests
from thinkup_cli.utils.file import update_rc_locally
from thinkup_cli.utils.firebase import REMOTE_CONFIG_URL, get_access_token, publish
from thinkup_cli.utils.ui import UI

def update_remote_config():
    headers = {
        'Authorization': 'Bearer ' + get_access_token()
    }
    resp = requests.get(REMOTE_CONFIG_URL, headers=headers)
    if resp.status_code == 200:
        with io.open('config.json', 'wb') as f:
            f.write(resp.text.encode('utf-8'))
        update_rc_locally()
        publish(resp.headers['ETag'])
    else:
        UI().perror(f'Unable to get template: {resp.text}')



