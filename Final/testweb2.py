import urllib
import urllib2

url = 'http://127.0.0.1:8080/EvenAbort'
values = {'group_name' : 'D'}

data = urllib.urlencode(values)
req = urllib2.Request(url, data)
response = urllib2.urlopen(req)
the_page = response.read()