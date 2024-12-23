from modules.config import *
from modules.fingerprints import user_agent, x_super_properties
import requests
from modules.ui import Logger

def get_cookies():
    try:
        headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.5",
            "connection": "keep-alive",
            "host": "canary.discord.com",
            "referer": "https://canary.discord.com/",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": user_agent,
            "x-context-properties": "eyJsb2NhdGlvbiI6IkFjY2VwdCBJbnZpdGUgUGFnZSJ9",
            "x-debug-options": "bugReporterEnabled",
            "x-discord-locale": "en-US",
            "x-super-properties": x_super_properties
        }
        
        response = requests.get(
            "https://canary.discord.com/api/v9/experiments", headers=headers
        )
        response.raise_for_status() 
        
        cookies = response.cookies
        cookie_string = ""
        
        for cookie_name, cookie_value in cookies.items():
            cookie_string += f"{cookie_name}={cookie_value}; "
        
       
        return cookie_string.rstrip("; ")
    
    except Exception as e:
        Logger.Error("Unable To Fetch Cookies", f"{e}")
        return None
