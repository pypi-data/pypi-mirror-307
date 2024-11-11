import requests
import json
from typing import Tuple, Dict
from .jwtutil import get_kid_from_jwt, get_name_with_company_subfix

def create_iap_edge_controller_app(url: str, client_name: str, info: str, authinfo: dict)-> Tuple[Dict, bool]: 
    try:
        kid = get_kid_from_jwt(authinfo['jwt'])
        data = {
            "clientName": client_name,
            "additionalInformation": {
                "info": info
            }
        }
        api_url = f"{url}/v1/device/shieldid/app/{kid}"
        response = requests.post(api_url, data=json.dumps(data), headers={"Content-Type": "application/json", "Authorization": f"Bearer {authinfo['jwt']}"})
        if response.status_code != 200:
            return {"error": f"Failed to create app: {response.text}"}, False
        return response.json(), True
    except Exception as e:
        return {"error": f"Error: {e}"}, False
