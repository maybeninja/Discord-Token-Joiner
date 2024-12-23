import os
import re
import random
import sys
import websocket
import string
import requests
import json
import concurrent.futures
import time
import ctypes
import threading
from datetime import datetime
from pytz import timezone
from modules.fingerprints import ja3_list
from modules.ui import Logger
from modules.cookies import get_cookies
from modules.config import delay, capsolving, threads, proxy, api_key
from tls_client import Session
import pystyle

captcha = 0
success = 0
failed = 0

def title():
    global success, failed, captcha
    t = f"Asta Token Joiner | Success: {success} | Failed: {failed} | Captcha: {captcha} | Total: {success + failed}"
    ctypes.windll.kernel32.SetConsoleTitleW(t)


def update_title_periodically():
    while True:
        title()
        time.sleep(1) 

output_folder = f"Output/{time.strftime('%Y-%m-%d %H-%M-%S')}"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def getclient():
    ja_prop = random.choice(ja3_list)
    chrome_version = str(random.randint(118, 129))

    session = Session(
        client_identifier=f"chrome_{chrome_version}",
        random_tls_extension_order=True,
    )

    x_super_properties = ja_prop.get("x-super-properties")
    user_agent = ja_prop.get("user-agent")

    return session, x_super_properties, user_agent

def format_invite(invite):
    pattern = r"(?:https?://)?(?:www\.)?(?:discord\.(?:com|gg)/(?:invite/)?|discordapp\.com/invite/)?([a-zA-Z0-9]+)"
    match = re.match(pattern, invite)
    return match.group(1) if match else None

class Joiner:
    def __init__(self):
        self.success = 0
        self.failed = 0
        self.captcha = 0
        self.headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json",
            "origin": "https://discord.com",
            "priority": "u=1, i",
            "referer": "https://discord.com/channels/@me",
            'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            "x-debug-options": "bugReporterEnabled",
            "x-discord-locale": "en-US",
            "x-discord-timezone": "Asia/Calcutta",
        }

    def join(self, email, password, token, invite):
        global success, captcha, failed

        session, x_super_properties, user_agent = getclient()

        self.headers["Authorization"] = token
        self.headers["user-agent"] = user_agent
        self.headers["x-super-properties"] = x_super_properties
        self.headers['cookie'] = get_cookies()
        self.headers['x-context-properties'] = 'eyJsb2NhdGlvbiI6IkpvaW4gR3VpbGQiLCJsb2NhdGlvbl9ndWlsZF9pZCI6IjExMTA0ODczNDYxOTQ5NDgxOTgiLCJsb2NhdGlvbl9jaGFubmVsX2lkIjoiMTI5MjAxODU3NTEwMzc1NDMwMiIsImxvY2F0aW9uX2NoYW5uZWxfdHlwZSI6MH0='

        try:
            response = session.post(
                f'https://discord.com/api/v9/invites/{invite}',
                headers=self.headers,
                json={}
            )

            if response.status_code == 200:
                Logger.Success(f'Joined: {token[:20]}', f'{invite}')
                with open(f"{output_folder}/success.txt", "a", encoding="utf-8") as success_file:
                    success_file.write(email + ":" + password + ":" + token + "\n")
                success += 1

            elif 'captcha_key' in response.text:
                Logger.Info(f'Captcha: {token[:20]}', f'{invite}')
                captcha += 1
                failed += 1
                Logger.Error(f'Captcha Solving Disabled: {token[:20]}', f'{invite}')
                with open(f"{output_folder}/failed.txt", "a", encoding="utf-8") as failed_file:
                    failed_file.write(email + ":" + password + ":" + token + "\n")

            

        except Exception as e:
            Logger.Error(f'Unable To Join: {token[:20]}', f'{str(e)}')
            failed += 1
            with open(f"{output_folder}/failed.txt", "a", encoding="utf-8") as failed_file:
                failed_file.write(email + ":" + password + ":" + token + "\n")

        title()

    def start(self, thread_limit, invite):
        with open('Input/tokens.txt') as file:
            auths = file.readlines()
            self.total = len(auths)
            with concurrent.futures.ThreadPoolExecutor(max_workers=thread_limit) as executor:
                futures = []
                for combo in auths:
                    combo = combo.strip()
                    email = combo.split(':')[0]
                    password = combo.split(':')[1]
                    token = combo.split(":")[2]
                    future = executor.submit(self.join, email, password, token, invite)
                    futures.append(future)
                for future in concurrent.futures.as_completed(futures):
                    future.result()

        time.sleep(delay)

if __name__ == "__main__":
    os.system("cls")
    threading.Thread(target=update_title_periodically, daemon=True).start()  # Start the title update thread

    banner = f"""

████████╗░█████╗░██╗░░██╗███████╗███╗░░██╗\u200b\u200b░░░░░██╗░█████╗░██╗███╗░░██╗███████╗██████╗░
╚══██╔══╝██╔══██╗██║░██╔╝██╔════╝████╗░██║\u200b\u200b░░░░░██║██╔══██╗██║████╗░██║██╔════╝██╔══██╗
░░░██║░░░██║░░██║█████═╝░█████╗░░██╔██╗██║\u200b\u200b░░░░░██║██║░░██║██║██╔██╗██║█████╗░░██████╔╝
░░░██║░░░██║░░██║██╔═██╗░██╔══╝░░██║╚████║\u200b\u200b██╗░░██║██║░░██║██║██║╚████║██╔══╝░░██╔══██╗
░░░██║░░░╚█████╔╝██║░╚██╗███████╗██║░╚███║\u200b\u200b╚█████╔╝╚█████╔╝██║██║░╚███║███████╗██║░░██║
░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚══╝\u200b\u200b░╚════╝░░╚════╝░╚═╝╚═╝░░╚══╝╚══════╝╚═╝░░╚═╝

Github: maybeninja
    """
    print(pystyle.Center.XCenter(pystyle.Colorate.Vertical(text=banner, color=pystyle.Colors.purple_to_blue), spaces=15))

    invite = input('Invite: ')

    invite = format_invite(invite)

    if not invite:
        print("Invalid invite format.")
        exit()

    j = Joiner()
    j.start(invite=invite, thread_limit=threads)
