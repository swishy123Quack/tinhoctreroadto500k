import subprocess
import threading
import requests
import random 
import string
import json
import time
import os

from bs4 import BeautifulSoup

USERNAME_POOL = ['TralaleroTralala', 'BombardiroCrocodillo', 'ChimpanziniBananini', 'BrrBrrPatapim', 'TrippiTroppi', 'UDinDunMaDinDinDinDun', 'TaTaTaTaTaTaTaSahur', 'FrigoCamelo']

REGISTER_URL = 'https://tinhoctre.vn/accounts/register/'
REGISTER_COMPLETE_URL = 'https://tinhoctre.vn/accounts/register/complete/'

NO_PROCESS = 1 # number of processes per account
NO_ACCOUNT = 30 # number of unique accounts

UPDATE_INTERVAL = 1.0 # seconds

def random_string(uppercase, lowercase, digits, punctuation):
    res = []
    for i in range(uppercase):
        res.append(random.choice(string.ascii_uppercase))
    for i in range(lowercase):
        res.append(random.choice(string.ascii_lowercase))
    for i in range(digits):
        res.append(random.choice(string.digits))
    for i in range(punctuation):
        res.append(random.choice(string.punctuation))
    random.shuffle(res)
    return ''.join(res)
        
def gen_account():
    name = random.choice(USERNAME_POOL)
    suffix = random_string(0, 0, 20, 0)
    username = name + suffix
    email = random_string(10, 10, 0, 0) + '@gmail.com'
    password = random_string(5, 5, 5, 5)
    
    while (len(username) > 30):
        username = username[:-1]
    print(f"\nGenerating account with [username = {username}], [password = {password}], [email = {email}]")
        
    session = requests.Session()
    resp = session.get(REGISTER_URL)

    soup = BeautifulSoup(resp.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
    
    register_form = {
        'csrfmiddlewaretoken': csrf_token,
        'full_name': name,
        'username': username,
        'email': email,
        'password1': password,
        'password2': password,
        'timezone': 'Asia/Ho_Chi_Minh',
        'language': '4',
    }
    headers = {
        'Referer': REGISTER_URL,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    resp = session.post(REGISTER_URL, data=register_form, headers=headers)
    if resp.url == REGISTER_COMPLETE_URL:
        print("Registration successful!")
        return {'username': username, 'password': password}
    else:
        print("Registration failed!")
        return None

def load_accounts():
    accounts = []
    with open('accounts.json', 'r') as file:
        accounts = json.load(file)
    return accounts['accounts']

def save_accounts(data):
    with open('accounts.json', 'w') as file:
        json.dump(data, file, indent=4)

def run_script(name, username, password, index):
    subprocess.run(
        ["python", name, "--username", username, "--password", password, "--id", index],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )    

def green(text):
    return f"\033[32m{text}\033[0m"

def red(text):
    return f"\033[31m{text}\033[0m"

def magenta(text):
    return f"\033[35m{text}\033[0m"

def blue(text):
    return f"\033[34m{text}\033[0m"

def yellow(text):
    return f"\033[33m{text}\033[0m"

def log_info():
    thread_infos = []
    for item in os.listdir('./logs'):
        full_path = os.path.join('./logs', item)
        if os.path.isfile(full_path):
            if not item.endswith('.json'):
                continue
            with open(full_path, 'r') as file:
                data = json.load(file)
                thread_infos.append(data)

    accumulated_speed = 0.0
    accumulated_submissions = 0
    
    for info in thread_infos:
        successful_submissions = info['successful_submissions']
        failed_submissions = info['failed_submissions']
        elapsed_time = info['elapsed_time']
        logged_in = info['logged_in']
        max_submissions = info['max_submissions']
        username = info['username']
        total_submissions = successful_submissions + failed_submissions
        speed = total_submissions / elapsed_time if elapsed_time > 0 else 0
        
        accumulated_speed += speed
        accumulated_submissions += total_submissions

        if logged_in == True:
            logged_in = green("YES")
        else:
            logged_in = red("NO")
        print("\033[K", end="")
        print(f"{yellow(f"Username: ")} {magenta(username)}, {yellow("Logged in: ")} {logged_in} {yellow('Success: ')} {green(successful_submissions)}, {yellow('Failed: ')} {red(failed_submissions)}, {yellow('Total: ')} [{total_submissions} / {max_submissions}], {yellow('Speed: ')} {speed:.2f}/s")

    print(f"\n{yellow('Total submissions: ')}{accumulated_submissions}, {yellow('Total speed: ')} {accumulated_speed:.2f}/s")
    print(f"\033[{len(thread_infos) + 2}A", end='')

def clear_logs():
    for item in os.listdir('./logs'):
        full_path = os.path.join('./logs', item)
        if os.path.isfile(full_path):
            os.remove(full_path)

accounts = load_accounts()
if len(accounts) < NO_ACCOUNT:
    print("Missing accounts in database, attempting to add...")
while len(accounts) < NO_ACCOUNT:
    account = gen_account()
    if account == None:
        print("Retrying...")
    else:
        accounts.append(account)
        
save_accounts({"accounts": accounts})
clear_logs()

threads = []
index = 0
for script in range(NO_ACCOUNT):
    for i in range(NO_PROCESS):
        t = threading.Thread(target=run_script, args=('run.py', accounts[index]["username"], accounts[index]["password"], str(index)))
        t.start()
        threads.append(t)
    index += 1

while True:
    thread_alive = False
    for t in threads:
        if t.is_alive():
            thread_alive = True
            break
    if not thread_alive:
        print("All threads have finished.")
        break
    log_info()
    time.sleep(UPDATE_INTERVAL)
