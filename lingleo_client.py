import requests
import urllib.parse
from config import leo_url
import json


class Base(object):
    def __init__(self):
        pass


class AuthorizeLeo(Base):

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.authorized = False
        self.cookies = self.__get_authorized_cookie()
        super(AuthorizeLeo, self).__init__()

    def __get_authorized_cookie(self):
        session = requests.Session()
        data = {'email': self.email, 'password': self.password}
        resp = session.post('%s/ru/login?%s' % (leo_url, urllib.parse.urlencode(data)))
        if 'login' in resp.url:
            self.authorized = False
            return
        cookies = ''
        for k, v in session.cookies.get_dict().items():
            cookies += '%s=%s;' % (k, v)
        self.authorized = True
        return cookies


class GetLeoDict(AuthorizeLeo):

    FILTER_ALL = 'all'
    FILTER_LEARNING = 'learning'
    FILTER_LEARNED = 'learned'
    FILTER_NEW = 'no_translate'

    def __init__(self, email, password):
        super(GetLeoDict, self).__init__(email, password)
        self.all_words = self.get_words()
        self.learning_words = self.get_words(self.FILTER_LEARNING)
        self.new_words = self.get_words(self.FILTER_NEW)
        self.learned_words = self.get_words(self.FILTER_LEARNED)

    def get_dirty_resp_from_leo(self, page, filter_words):
        data = {'sortBy': 'date',
                'wordType': '0',
                'filter': filter_words,
                'page': page,
                'groupId': 'dictionary'}

        headers = {'Accept': '*/*',
                   'Accept-Encoding': 'gzip, deflate',
                   'Connection': 'keep-alive',
                   'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                   'Host': 'lingualeo.com',
                   'Origin': leo_url,
                   'Cookie': self.cookies,
                   'Referer': '%s/ru/glossary/learn/dictionary' % leo_url,
                   'X-Requested-With': 'XMLHttpRequest'}
        dictionary_page = requests.post(url='%s/userdict/json' % leo_url,
                                        headers=headers, data=data)
        return json.loads(dictionary_page.text)

    def get_words(self, filter_words='all'):
        """:param: filter_words : all, learning, no_translate (new), learned"""
        if not self.authorized:
            return []
        state = True
        page = 1
        words = []
        while state:
            resp = self.get_dirty_resp_from_leo(page, filter_words)
            for key in resp.keys():
                if 'userdict' in key:
                    if not resp[key]:
                        state = False
                    for lst in resp[key]:
                        for k, v in lst.items():
                            if k == 'words':
                                for word in v:
                                    translated = list(map(lambda obj: obj['translate_value'],
                                                          word['user_translates']))
                                    words.append({'id': word['word_id'],
                                                  'en_name': word['word_value'],
                                                  'translated': ','.join(translated)})
            page += 1
        return words

leo = GetLeoDict('spaun1002@gmail.com', '7847473')
