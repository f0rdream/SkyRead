import requests
import json
def get_access_token():
    api ="https://api.weixin.qq.com/cgi-bin/token?" \
         "grant_type=client_credential" \
         "&appid=wx3dd514b1ed8d2610" \
         "&secret=a386ecb287752ea6b3a21ed000a711cf"
    response = requests.get(api)
    if response.status_code == 200:
        return response.json()['access_token']

def get_ticket():
    api = "https://api.weixin.qq.com/cgi-bin/ticket/getticket?" \
          "access_token="+get_access_token()+"&type=jsapi"
    response = requests.get(api)
    if response.status_code == 200:
        dict = json.loads(response.text)
        return dict['ticket']
print get_ticket()