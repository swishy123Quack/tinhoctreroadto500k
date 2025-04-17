import requests
import time

from bs4 import BeautifulSoup

session = requests.Session()

USERNAME = 'UltimateWiener' 
PASSWORD = 'T43r@6pqUJCKYLH' 

LOGIN_URL = 'https://tinhoctre.vn/accounts/login/' 
SUBMIT_URL = 'https://tinhoctre.vn/problem/digit/submit'

MAX_SUBMISSIONS = 10
SUBMISSION_DELAY = 1.0 # seconds

def login():
    login_url = LOGIN_URL
    resp = session.get(login_url)

    soup = BeautifulSoup(resp.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']

    login_form = {
        'username': USERNAME,
        'password': PASSWORD,
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
        print("Submission failed!")
    else:
        print(resp.url)

login()
print("Begin nuking")
for i in range(MAX_SUBMISSIONS):
    time.sleep(SUBMISSION_DELAY)
    submit()