import requests
import threading
import re
import time
from lxml import etree

class FB(object):
    
    def __init__(self, x, y, z = False):
        self._resources = dict()
        self._manager = z
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
        self._resources["credentials"] = dict()
        self._resources["credentials"]["email"] = x
        self._resources["credentials"]["password"] = y
        self._resources["uid"] = None
        self._resources["cookies"] = None
        self._threads = dict()
        self._session = requests.Session()
        self._session.headers["User-Agent"] = self._resources["User-Agent"]
        self._doPing = False
        self._running  = False
        
    def init(self):
        x = self._resources["credentials"]["email"]
        y = self._resources["credentials"]["password"]
        self._threads["main"] = threading.Thread(target = self._init, args = (x, y))
        self._threads["main"].daemon = True
        self._threads["main"].start()
        
    def _init(self, x, y):
        form = etree.HTML(self._session.get(self._resources["login-url"]).text).xpath('//form[@id="login_form"][1]')
        if form:
            form_data = dict()
            for x in form[0].xpath('.//input'):
                if x.xpath('@name[1]') and x.xpath('@value[1]'):
                    form_data.update({x.xpath('@name[1]')[0]: x.xpath('@value[1]')[0]})
            self._resources["login-form-values"] = form_data
            self._resources["login-form-values"]["email"] = self._resources["credentials"]["email"]
            self._resources["login-form-values"]["pass"] = self._resources["credentials"]["password"]
            self._resources["cookies"] = dict()
            self._resources["cookies"]["_js_reg_fb_ref"] = "https%3A%2F%2Fwww.facebook.com%2F"
            self._resources["cookies"]["_js_reg_fb_gate"] = "https%3A%2F%2Fwww.facebook.com%2F"
            self._resources["cookies"]["_js_datr"] = self._regInstance(self._session.get(self._resources["base-url"]).text)
            post = self._session.post(self._resources["login-url"], data = self._resources["login-form-values"], cookies = self._resources["cookies"])
            self._resources["uid"] = self._uid(post.text)
            self._resources["ping-parameters"]["channel"] = self._resources["ping-parameters"]["channel"] + self._resources["uid"]
            self._resources["ping-parameters"]["uid"] = self._resources["ping-parameters"]["uid"] + self._resources["uid"]
            self._resources["ping-parameters"]["viewer_uid"] = self._resources["ping-parameters"]["viewer_uid"] + self._resources["uid"]
            self._resources["dtsg"] = self._dtsg(post.text)
        else:
            raise Exception("Something went wrong: No form was found for login")
        
    def _regInstance(self, data):
        try:
            regInstance = etree.HTML(data).xpath('//input[@id="reg_instance"]/@value')[0]
            return regInstance
        except Exception as e:
            raise Exception("Unable to return reg_instance value: " + str(e))
            
    def _ping(self, interval = 2):
        while self._doPing:
            self.ping()
            time.sleep(interval)
            return    
            
    def _uid(self, data):
        uid = re.search('\"USER_ID\":\"(\d+)\"', data)
        if uid and str(uid.group(1)) != "0":     
            return uid.group(1)
        else:
            raise Exception("Unable to gather user id, Probable cause: INVALID LOGIN CREDENTIALS")
            
    def _dtsg(self, data):
        dtsg = re.search('name=\"fb_dtsg\" value=\"(.*?)\"', data)
        if dtsg and str(dtsg.group(1)) != "0":
            return dtsg.group(1)
        else:
            raise Exception("Unable to gather dtsg value")
         
    def _unlink(self):
        self._session.close()
        self._doPing = False
        del self._threads["main"]
        return
    
    def ping(self):
        return
        
                
class Manager(object):
    
    def __init__(self, x, y):
        self.running = False
        self.fb = FB(x, y, self)
        
    def link(self):
        self.fb.init()
        self.running = True
        
    def close(self):
        self.fb._unlink()
        self.running = False
        return
        
    def ping(self):
        if self.running:
            self.fb.ping()
        else:
            print("Facebook instance isn't running")
            