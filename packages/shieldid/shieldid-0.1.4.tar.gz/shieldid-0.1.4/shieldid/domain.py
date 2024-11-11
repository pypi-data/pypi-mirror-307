import requests
from typing import Tuple, Dict
from .jwtutil import get_kid_from_jwt
import urllib.parse

def prepare_api_parameter(parameter: str) -> str:
    encoded_parameter = urllib.parse.quote(parameter)
    return encoded_parameter

def set_dns_record(url: str, name: str, ip_address: str,  authinfo: dict)-> Tuple[Dict, bool]: 
    try:
        kid = get_kid_from_jwt(authinfo['jwt'])
        new_name = prepare_api_parameter(name)
        new_ip_address = prepare_api_parameter(ip_address)
        api_url = f"{url}/v1/domain/dns/{kid}?name={new_name}&ip_address={new_ip_address}"
        response = requests.post(api_url, data='', headers={"Content-Type": "application/json", "Authorization": f"Bearer {authinfo['jwt']}"})
        if response.status_code != 200:
            print(response.text)
            return {"error": f"Failed to create app: {response.text}"}, False
        return response.json(), True
    except Exception as e:
        return {"error": f"Error: {e}"}, False

def make_ssl_certificates(url: str, full_domain_name_with_wildcard: str,  authinfo: dict)-> Tuple[Dict, bool]: 
    try:
        kid = get_kid_from_jwt(authinfo['jwt'])
        new_name = prepare_api_parameter(full_domain_name_with_wildcard)
        api_url = f"{url}/v1/domain/issue-cert/{kid}?name={new_name}"
        response = requests.post(api_url, data='', headers={"Content-Type": "application/json", "Authorization": f"Bearer {authinfo['jwt']}"})
        if response.status_code != 200:
            print(response.text)
            return {"error": f"Failed to create app: {response.text}"}, False
        return response.json(), True
    except Exception as e:
        return {"error": f"Error: {e}"}, False


    
    
