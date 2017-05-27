import re
import os
import sys
import json
import urllib
import requests
import operator
from datetime import datetime
from collections import Counter
from bs4 import BeautifulSoup as bs

def doHelloMessage():
   alert('hello')
doHelloMessage()

def login():
    # Starts the session
    session = requests.Session()
    # Opens the Facebook login page in the session
    homepage_response = session.get('https://www.facebook.com/').text
    # Loads the login page into a BeautifulSoup soup object
    soup = bs(homepage_response, "html5lib")
    # Extracts the LSD token from Facebook login page, required for login post request
    lsd = str(soup.find_all('input', attrs={"name": "lsd"})[0]['value'])

    # Login data for the Login POST request
    login_data = {
    'email': username,
    'pass': password,
    'locale': 'en_US',
    'non_com_login': '',
    'lsd': lsd
    }
    # URL for the login POST request
    login_url = 'https://login.facebook.com/login.php?login_attempt=1'
    # Logs in and stores the response page (our Facebook home feed)
    content = session.post(login_url, data=login_data, verify=False).content


login()

# modify html page
document.getElementById("result").innerHTML = 'Compiled Python script in Chrome'


# write into log
console.log('hello from python')
