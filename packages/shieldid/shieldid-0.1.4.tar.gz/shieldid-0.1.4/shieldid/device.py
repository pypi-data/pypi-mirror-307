import time
import requests
from uuid import uuid4
from typing import Tuple, Dict, Callable
import progressbar

def default_show_url(url: str,user_code: str):
    print(f"Please visit \n\n{url}/{user_code} \n\nto log in.\n\n")
    print("Waiting for login...")    
    

def device_authorization(base_url: str, show_url: Callable = default_show_url) -> Tuple[Dict, bool]:
    """
    Perform device authorization for an SHIELD ID(Security365 Idaas) OAuth2 flow.

    Args:
        base_url (str): The base URL of the authorization server.
        show_url (Callable str, str): A function that will be called to show the user the URL to visit for login. 

    Returns:
        Dict: The response data from the authorization server.
        bool: True if the process is successful, otherwise False.

    Examples:
        [OK]
        {
            "access_token": "Fw9zvw...",
            "token_type": "bearer",
            "refresh_token": "4DZEq...",
            "expires_in": 3599,
            "scope": "read",
            "jwt": "eyJ0eXAiO..."
        }
        True
        
        [NOT OK]
        {
            "error": "reason"
        }
        False
    """    
    try:    
        pbar = None
        client_id = uuid4().hex
        device_authorization_start_endpoint = base_url +'/v1/device/code'
        token_endpoint = base_url + '/v1/device/token'
        
        response = requests.post(device_authorization_start_endpoint, json={
            'client_id': client_id,
            'scope': 'profile'
        })

        if response.status_code != 200:
            return { "error":"Failed to request device and user codes."}, False

        response_data = response.json()
        device_code = response_data.get('device_code')
        user_code = response_data.get('user_code')
        verification_uri = response_data.get('verification_uri')
        expires_in = response_data.get('expires_in')
        interval = response_data.get('interval', 5)
        
        # Check if any required response data is missing
        if not all([device_code, user_code, verification_uri, expires_in, interval]):
            return {"error": "Missing required data from response."}, False
        show_url(verification_uri, user_code)        
        
        widgets = [progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage(), ' ', progressbar.ETA()]
        pbar = progressbar.ProgressBar(maxval=expires_in, widgets=widgets).start()

        start_time = time.time()
        while time.time() - start_time < expires_in:
            response = requests.post(token_endpoint, json={
                'client_id': client_id,
                'device_code': device_code
            })
            if response.status_code == 200:
                return response.json(), True
            elif response.status_code == 204:
                progress_time = int(time.time() - start_time)
                pbar.update( progress_time)
                time.sleep(interval)            
            else:
                return {"error":f"Unexpected error: {response.status_code}"}, False
        return {"error":"Authorization timed out."}, False
    except Exception as e:
        print(f"Error: {e}")
        return {"error":f"Error: {e}"}, False
    finally:
        if(pbar):
            pbar.finish()

