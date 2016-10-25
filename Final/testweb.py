import urllib2
response = urllib2.urlopen('http://127.0.0.1:8080/Get_Status_Project')
html = response.read()
print html