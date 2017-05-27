import urllib2
import urllib
import gzip
import os
import json
import sys
import time
import StringIO

if len(sys.argv) <= 1:
	print "Usage:\n 	python dumper.py [conversation ID] [chunk_size (recommended: 2000)] [{optional} offset location (default: 0)]"
	print "Example conversation with Raghav Sood"
	print "	python dumper.py 1075686392 2000 0"
	sys.exit()

error_timeout = 30 # Change this to alter error timeout (seconds)
general_timeout = 7 # Change this to alter waiting time afetr every request (seconds)
messages = []
talk = sys.argv[1]
offset = int(sys.argv[3]) if len(sys.argv) >= 4 else int("0")
messages_data = "lolno"
end_mark = "\"payload\":{\"end_of_history\""
limit = int(sys.argv[2])
headers = {"origin": "https://www.facebook.com", 
"accept-encoding": "gzip,deflate", 
"accept-language": "en-US,en;q=0.8", 
"cookie": "datr=boQpWQ1AjUeLF9oaWPpF4nX0; dats=1; sb=poQpWRANeN7Q44kkvc3tKB1W; c_user=100017385199158; xs=38%3AeUl7ZW9VIpp18Q%3A2%3A1495893158%3A-1; fr=0P4uUtaecW0gJCVPR.AWWIh18Qzdrss-c5UaaCeJv__rQ.BZKYRu.85.AAA.0.0.BZKYSm.AWVdJc2L; pl=n; lu=gA; act=1495893266256%2F3; presence=EDvF3EtimeF1495893271EuserFA21B17385199158A2EstateFDutF1495893271686CEchFDp_5f1B17385199158F2CC", 
"pragma": "no-cache", 
"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.122 Safari/537.36", 
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

while end_mark not in messages_data:

	data_text = {"messages[user_ids][" + str(talk) + "][offset]": str(offset), 
	"messages[user_ids][" + str(talk) + "][limit]": str(limit), 
	"client": "web_messenger", 
	"__user": "100017385199158", 
	"__a": "1", 
        "__dyn": "7AzkXh8OAcjxd2u6aOGeFxqewRAKGgS8zAS-C11xG3F6wAxu13wFGEa8Gm4UJi28rxuF8vDKuEjKexKcxaFQ3uaVVojxC4oKLGqu58nUszaxbxm1iyECQum2m4oqyUfe5FHxuvgqxKVUoh8CrzEly8myEbQm5EgAwzCwYypUhKHxiiq4UC8Gez8O784afBxm9yUvy8lw", 
	"__req": "g", 
        "fb_dtsg": "AQFyQXYY-_SE:AQFHPlGORqti", 
	"ttstamp": "1495890587525", 
	"__rev": "3050022"}
	data = urllib.urlencode(data_text)
	url = "https://www.facebook.com/ajax/mercury/thread_info.php"
	
	print "Retrieving messages " + str(offset) + "-" + str(limit+offset) + " for conversation ID " + str(talk)
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
			messages = messages + json_data['payload']['actions']
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
command = "python -mjson.tool " + directory + "complete.json > " + pretty_directory + "complete.pretty.json"
os.system(command)
