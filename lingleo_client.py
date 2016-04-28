import requests
import urllib.parse

session = requests.Session()
data = {'email': 'spaun1002@gmail.com', 'password': '7847473'}
session.post('http://lingualeo.com/ru/login?%s' % urllib.parse.urlencode(data))
cookies = ''
for key, value in session.cookies.get_dict().items():
    cookies += '%s=%s;' % (key, value)
print(cookies)
headers = {'Accept': '*/*',
           'Cache-Control': 'no-cache',
           'Cookie': cookies}
dictionary_page = requests.get(url='http://lingualeo.com/ru/glossary/learn/dictionary',
                               headers=headers)
# print(dictionary_page.text)


data = {'sortBy': 'date',
        'wordType': '0',
        'filter': 'all',
        'page': '1',
        'groupId': 'dictionary'}
headers = {'Accept': '*/*',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'en,uk;q=0.8,en-US;q=0.6,ru;q=0.4',
           'Connection': 'keep-alive',
           'Content-Length': '59',
           'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
           'Host': 'lingualeo.com',
           'Origin': 'http://lingualeo.com',
           'Cookie': cookies,
           'Referer': 'http://lingualeo.com/ru/glossary/learn/dictionary',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/49.0.2623.112 Safari/537.36',
           'X-Requested-With': 'XMLHttpRequest'}
req = requests.post(url='http://lingualeo.com/userdict/json', headers=headers, data=data)
print(req.text)
