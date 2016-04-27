import requests
import threading
from lxml import etree

class FB(object):
    
    def __init__(self, x, y, z = False):
        self._resources = dict()
        self._resources["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36"
        self._resources["base-url"] = "https://www.facebook.com/"
        self._resources["login-url"] = self._resources["base-url"] + "login.php"
        self._resources["ping-url"] = "https://0-channel-proxy-06-ash2.facebook.com/active_ping"
        self._resources["ping-parameters"] = dict()
        self._resources["ping-parameters"]["channel"] = "p_"
        self._resources["ping-parameters"]["partition"] = "-2"
        self._resources["ping-parameters"]["clientid"] = "5ae4ed0b"
        self._resources["ping-parameters"]["cb"] = "el2p"
        self._resources["ping-parameters"]["cap"] = "0"
        self._resources["ping-parameters"]["uid"] = ""
        self._resources["ping-parameters"]["viewer_uid"] = ""
        self._resources["ping-parameters"]["sticky_token"] = "479"
        self._resources["ping-parameters"]["state"] = "active"
        self._resources["uid"] = None
        self._threads = dict()
        self._session = requests.Session()
        self._session.headers["User-Agent"] = self._resources["User-Agent"]
        self._pingThread = None
        self._thread = threading.Thread(target = self._init, args = (x, y))
        self._thread.daemon = True
        self._thread.start()
        
        
    def _init(self, x, y):
        form = etree.HTML(self._session.get(self._resources["login-url"]).text).xpath('//form[@id="login_form"][1]')
        if form:
            form_data = dict()
            for x in form[0].xpath('.//input'):
                if x.xpath('@name[1]') and x.xpath('@value[1]'):
                    form_data.update({x.xpath('@name[1]')[0]: x.xpath('@value[1]')[0]})
            self._resources["login-form-values"] = form_data
        else:
            raise Exception("Something went wrong: No form was found for login")
        return
