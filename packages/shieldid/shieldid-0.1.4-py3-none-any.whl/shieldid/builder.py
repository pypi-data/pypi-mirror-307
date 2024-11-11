from .device import device_authorization
from .app import create_iap_edge_controller_app
from .jwtutil import get_kid_from_jwt, get_name_with_company_subfix
from .domain import set_dns_record, make_ssl_certificates
from typing import Tuple, Callable, Dict
import re
import json

class EdgeInfoObject:
    def __init__(self, auth_info: Dict , app_info: Dict, etc_info: Dict):
        self.auth_info = auth_info or {}
        self.app_info = app_info or {}
        self.etc_info = etc_info or {}

    def __str__(self):
        return (f'auth_info: {json.dumps(self.auth_info,indent =2)}\n'
                f'app_info: {json.dumps(self.app_info,indent =2)}\n'
                f'ect_info: {json.dumps(self.etc_info,indent =2)}\n')
    def get_jwt(self) -> str:
        """get SHIELD ID jwt token. use after device authorization flow
        Returns:
            str: jwt token
        """
        return self.auth_info.get('jwt', '')
    def get_company_id(self) -> str:
        """get SHIELD ID company id. use after device authorization flow
        Returns:
            str: company id
        """
        return self.etc_info.get('company_id', '')
    def get_access_token(self) -> str:
        """get SHIELD ID access token. use after device authorization flow
        Returns:
            str: access token
        """
        return self.auth_info.get('access_token', '')
    def get_refresh_token(self) -> str:
        """get SHIELD ID access token. use after device authorization flow
        Returns:
            str: access token
        """
        return self.auth_info.get('refresh_token', '')
    def get_app_id(self) -> str:
        """get SHIELD ID app clientId. use after create_edge_app or create_app
        Returns:
            str: clientId
        """
        return self.app_info.get('msg', {}).get('clientId', '')
    def get_app_secret(self) -> str:
        """get SHIELD ID app clientSecret. use after create_edge_app or create_app
        Returns:
            str: clientSecret
        """
        return self.app_info.get('msg', {}).get('clientSecret', '')
    def get_app_extra(self) -> str:
        """get SHIELD ID app company id. use after create_edge_app or create_app
        Returns:
            str: companyId for app belongs to
        """
        return self.etc_info.get('company_id', '')
    def get_app_name(self) -> str:
        """get SHIELD ID app clientName. use after create_edge_app or create_app
        Returns:
            str: clientName
        """
        return self.etc_info.get('app_name', '')
    def get_ip_address(self) -> str:
        """get SHIELD ID app ip address. use after set_dns_record
        Returns:
            str: ip address
        """
        return self.etc_info.get('ip_address', '')
    def get_main_domain(self) -> str:
        """get SHIELD ID app main domain. use after set_dns_record
        Returns:
            str: main domain
        """
        return self.etc_info.get('main_domain', '')
    def get_fullchain(self) -> str:
        """get SHIELD ID app fullchain. use after make_ssl_certificates
        Returns:
            str: fullchain
        """
        return self.etc_info.get('fullchain', '')
    def get_privkey(self) -> str:
        """get SHIELD ID app privkey. use after make_ssl_certificates
        Returns:
            str: privkey
        """
        return self.etc_info.get('privkey', '')


def is_valid_base_name(input_string: str) -> bool:
    if len(input_string) > 12:
        return False
    pattern = re.compile("^[a-zA-Z0-9]*$")
    if pattern.match(input_string):
        return True
    else:
        return False

DEFAULT_BASE_DOMAIN = "idproxy.stream"
STEP_INIT = 0 
STEP_DEVICE_AUTHORIZATION = 1
STEP_CREATE_APP = 2
STEP_SET_DNS_RECORD = 3
STEP_MAKE_SSL_CERTIFICATES = 4


def default_show_url(url: str,user_code: str):
    print(f"Please visit \n\n{url}/{user_code} \n\nto log in.\n\n")
    print("Waiting for login.")    

class IapBuilder:
    def __init__(self):
        self.auth_info = {}
        self.app_info = {}

        self.company_id = ""
        self.app_name = ""
        self.full_name = ""
        self.main_domain = ""
        self.ip_address = ""
        self.valid = True
        self.last_error = ""
        self.step = 0
        self.url = ""
        self.fullchain = ""
        self.privkey = ""
    
    def set_last_error(self, error: str):
        self.last_error = error

    def device_authorize(self, url: str, show_url: Callable = default_show_url):
        self.url = url
        if not self.valid:
            return self
        self.auth_info, ok = device_authorization(url, show_url)
        if not ok:
            self.valid = False
            self.set_last_error("Device authorization failed.")
        else:
            self.step = STEP_DEVICE_AUTHORIZATION
            self.company_id = get_kid_from_jwt(self.auth_info['jwt'])
        return self

    def create_edge_app(self, base_name: str, info: str):
        # Check if base name is valid
        if not is_valid_base_name(base_name):
            self.valid = False
            self.set_last_error("Invalid base name. base name should be alphanumeric and less than 12 characters.")
            return self

        # Check if the builder is in a valid state        
        if not self.valid:
            return self

        #require device authorization flow to create edge app
        if self.step < STEP_DEVICE_AUTHORIZATION:
            self.valid = False
            self.set_last_error("create shieldid app require device authorization")
            return self
        
        new_base_name = get_name_with_company_subfix(base_name, self.company_id)
        self.base_name = new_base_name
        self.app_name = "iap-edge-" + new_base_name
        self.app_info, ok = create_iap_edge_controller_app(self.url, self.app_name, info, self.auth_info)
        
        if not ok:
            self.valid = False
            self.set_last_error("Create edge app failed.")
        else:
            self.step = STEP_CREATE_APP
        return self


    def set_dns_record(self, ip_address: str, base_domain: str = DEFAULT_BASE_DOMAIN):
        if not self.valid:
            return self
        if self.step < STEP_DEVICE_AUTHORIZATION:
            self.valid = False
            self.set_last_error("set dns record require device authorization")
            return self
        main_domain = f"{self.base_name}.{base_domain}"
        full_name = f"*.{main_domain}"
        _, ok = set_dns_record(self.url, full_name, ip_address, self.auth_info)
        
        if not ok:
            self.valid = False
            self.set_last_error("Set DNS record failed.")
        else:
            self.step = STEP_SET_DNS_RECORD
            self.ip_address = ip_address
            self.full_name = full_name
            self.main_domain = main_domain
        return self
    
    def make_ssl_certificates(self):    
        if not self.valid:
            return self
        if self.step < STEP_SET_DNS_RECORD:
            self.valid = False
            self.set_last_error("make_ssl_certificates require set dns record")
            return self
        info, ok = make_ssl_certificates(self.url, self.full_name, self.auth_info)
        if not ok:
            self.valid = False
            self.set_last_error("make_ssl_certificates failed.")
        else:
            self.step = STEP_MAKE_SSL_CERTIFICATES
            self.fullchain = info['cert']
            self.privkey = info['key']
        return self

    def build(self) -> Tuple[EdgeInfoObject, bool, str]:
        etc_info = {
            "company_id": self.company_id,
            "app_name": self.app_name,
            "main_domain": self.main_domain,
            "ip_address": self.ip_address,
            "fullchain": self.fullchain,
            "privkey": self.privkey
        }
        return EdgeInfoObject(self.auth_info, self.app_info, etc_info), self.valid, self.last_error