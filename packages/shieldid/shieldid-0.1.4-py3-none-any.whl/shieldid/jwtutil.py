import base64
import json
from typing import Optional

def get_kid_from_jwt(jwt_token: str) -> Optional[str]:
    """
    Extract the 'kid' value from the header of a JWT token.
    Args:
        jwt_token (str): The JWT token from which to extract the 'kid' value.
    Returns:
        Optional[str]: The 'kid' value if present, otherwise None.
    """
    try:
        header_b64 = jwt_token.split('.')[0]
        header_b64 += '=' * (-len(header_b64) % 4)
        header_json = base64.urlsafe_b64decode(header_b64).decode('utf-8')
        header_data = json.loads(header_json)
        return header_data.get('kid')
    except (IndexError, ValueError) as e:
        print(f"Error extracting 'kid' from JWT: {e}")
        return None

def lowercase_first_nlength(s: str, length: int = 5 ) -> str:
    if len(s) < length:
        return s.lower()
    else:
        return s[:length].lower()

def get_name_with_company_subfix(basename: str, company_id: str) -> str:
    lower_name = basename.lower()
    short = lowercase_first_nlength(company_id, 5)
    return f"{lower_name}-{short}"
