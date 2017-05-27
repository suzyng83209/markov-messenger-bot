'''
Get all of your friend's facebook user ids from your messaging history.
Usage: python get_friends.py <username> <password> <output file>

The output has the following format: id \t name \t username
Uses a browser automation library and the Phantom JS browser.
brew install phantomjs
pip install splinter
'''

import sys
import json
import time
import selenium
import requests
from splinter import Browser
from urllib2 import URLError

_base_url = "https://www.facebook.com"
_login_url = "https://login.facebook.com/login.php?login_attempt=1"
_base_msg_url = _base_url + "/messages/"

try:
	username = sys.argv[1]
	password = sys.argv[2]
	out = sys.argv[3]
except IndexError:
	print "Usage: python get_friends.py <username> <password> <output file>"
	sys.exit()

# Create the phantom js browser instance
browser = Browser("phantomjs")

# Log in by finding the log in form and filling it
# with your username and password. Then automatically
# "click" on the enter button, and navigate to the
# messages page.
def login():
	browser.visit(_base_url)
	# print browser
	# import pdb; pdb.set_trace();
	# email = browser.find_by_name("email")[0].find_by_tag("input")
	email = browser.find_by_name("email")
	email.fill(username)
 	passInput = browser.find_by_name("pass")
 # 	password = browser.find_by_name("pass")[0].find_by_tag("input")
	passInput.fill(password)

	enter = browser.find_by_value("Log In").first
	enter.click()
	print "Logged in!"

	browser.visit(_base_msg_url)

# This is the automatic equivalent of scrolling up.
def load_more():
	# Messages are contained within these divs
	import pdb; pdb.set_trace();

	pagers = browser.find_by_css("#uiScrollableAreaContent")[0].find_by_css("div.uiMorePager")
	for div in pagers:
		# The 'load more' area is really an a href tag, which can be 'clicked' on
		link = div.find_by_css("div")[0].find_by_css("a")[0]
		if link.value == 'Load Older Threads':
			print 'Loading more...'
			link.click()
			return True

# Once all threads have been loaded, call this function to
# get all the user ids and save them to a file.
def get_threads():
	f = open(out, 'w')
	# Each thread is stored in a list element with class _k-
	import pdb; pdb.set_trace();
	users = browser.find_by_css("ul")
	for user in users:
		try:
			fid = user['id']	# Your friend's id
			
			name = user.find_by_css("span._1ht6").text.lower() 	# Your friend's name
			username = user.find_by_css("a._1ht5 _2il3 _5l-3")['href'].split("/")[-1]		# Your friend's username (what appears in their url)

			f.write(str(fid) + '\t' + name.encode("utf8") + '\t' + username.encode("utf8") + '\n')
		except IndexError:
			pass

	print "written"

	f.close()

# Log in to Facebook
login()

# Keep loading new threads
# while True:
# 	try:
# 		loaded_more = load_more()
# 		if not loaded_more:
# 			break
# 		time.sleep(1)
# 	except (URLError, selenium.common.exceptions.StaleElementReferenceException):
# 		print "reconnecting......"
# 		# Try to reconnect
# 		time.sleep(5)
# 		try:
# 			login()
# 		except:
# 			continue

# Now that all threads have been loaded in the HTML,
# get all your friends' information
get_threads()
