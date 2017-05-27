import urllib2
import urllib
import gzip
import os
import json
import sys
import time
import StringIO

import config

__author__ = "Raghav Sood"
__copyright__ = "Copyright 2014"
__credits__ = ["Raghav Sood"]
__license__ = "CC"
__version__ = "1.0"
__maintainer__ = "Raghav Sood"
__email__ = "raghavsood@appaholics.in"
__status__ = "Production"

if len(sys.argv) <= 1:
    print "Usage:\n     python dumper.py [conversation ID] [chunk_size (recommended: 2000)] [{optional} offset location (default: 0)]"
    print "Example conversation with Raghav Sood"
    print " python dumper.py 1075686392 2000 0"
    sys.exit()

error_timeout = 30 # Change this to alter error timeout (seconds)
general_timeout = 7 # Change this to alter waiting time afetr every request (seconds)
messages = []
talk = sys.argv[1]
offset = int(sys.argv[3]) if len(sys.argv) >= 4 else int("0")
timestamp = int("0")
messages_data = "lolno"
end_mark = "\"payload\":{\"end_of_history\""
limit = int(sys.argv[2])
headers = {"origin": "https://www.facebook.com",
           "accept-encoding": "gzip,deflate",
           "accept-language": "en-US,en;q=0.8",
           "cookie": config.cookie,
           "pragma": "no-cache",
           "user-agent": " Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.107 Safari/537.36",
           "content-type": "application/x-www-form-urlencoded",
           "accept": "*/*",
           "cache-control": "no-cache",
           "referer": "https://www.facebook.com/messages/zuck"}

base_directory = "Messages/"
directory = base_directory + str(talk) + "/"
pretty_directory = base_directory + str(talk) + "/Pretty/"

try:
    os.makedirs(directory)
except OSError:
    pass # already exists

try:
    os.makedirs(pretty_directory)
except OSError:
    pass # already exists

while end_mark not in messages_data and offset < 50000:

    data_text = {"messages[user_ids][" + str(talk) + "][offset]": str(offset),
    "messages[user_ids][" + str(talk) + "][limit]": str(limit),
        "messages[user_ids]["+ str(talk) + "][timestamp]": str(timestamp),
    "client": "web_messenger",
    "__user": config.user,
    "__a": config.a,
    "__dyn": config.dyn,
	"__req": config.req,
    "fb_dtsg": config.fb_dtsg,
	"ttstamp": config.ttstamp,
	"__rev": config.rev}

    data = urllib.urlencode(data_text)
    url = "https://www.facebook.com/ajax/mercury/thread_info.php"

    req = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(req)
    compressed = StringIO.StringIO(response.read())
    decompressedFile = gzip.GzipFile(fileobj=compressed)


    outfile = open(directory + str(offset) + "-" + str(limit+offset) + ".json", 'w')
    messages_data = decompressedFile.read()
    messages_data = messages_data[9:]
    json_data = json.loads(messages_data)
    if json_data is not None and json_data['payload'] is not None:
        try:
            messages = json_data['payload']['actions'] + messages
            timestamp = int(json_data['payload']['actions'][0]['timestamp']) - 1
        except KeyError:
            pass #no more messages
    else:
        print "Error in retrieval. Retrying after " + str(error_timeout) + "s"
        print "Data Dump:"
        print json_data
        time.sleep(error_timeout)
        continue
    outfile.write(messages_data)
    outfile.close()
    command = "python -mjson.tool " + directory + str(offset) + "-" + str(limit+offset) + ".json > " + pretty_directory + str(offset) + "-" + str(limit+offset) + ".pretty.json"
    os.system(command)
    offset = offset + limit
    time.sleep(general_timeout)

finalfile = open(directory + "complete.json", 'wb')
finalfile.write(json.dumps(messages))
finalfile.close()
command = "python -mjson.tool " + directory + "complete.json > " + pretty_directory + "complete-pretty.json"
os.system(command)
