from typing import Optional, Union
import urllib3
import json

from requests.utils import dict_from_cookiejar, cookiejar_from_dict
from requests import Session

from wmain.requests.url import WUrl
from wmain.requests.response import WResponse
from wmain.requests.easy_ua import get_random

urllib3.disable_warnings()


class WRequestINI:
    headers: Optional[dict]
    timeout: Optional[int]
    proxies: Optional[dict]
    verify: Optional[bool]
    files: Optional[dict]

    def __init__(self):
        self.headers = {}
        self.timeout = None
        self.proxies = {}
        self.verify = False
        self.files = {}
        self.set_ua()

    def set_proxy(self, port: Union[int, str], ip: str = "127.0.0.1"):
        self.proxies = {"http": f"{ip}:{port}", "https": f"{ip}:{port}"}

    def set_ua(self, platform: str = "win"):
        self.headers["User-Agent"] = get_random(platform)


class WSession:

    def __init__(self):
        self.session = Session()
        self.ini = WRequestINI()

    def __dic(self, ini: WRequestINI, **kwargs):
        dic: dict = self.ini.__dict__.copy()
        if ini:
            dic.update(ini.__dict__)
        for key, value in kwargs.items():
            if isinstance(value, dict) and key in dic:
                dic[key].update(value)
            else:
                dic[key] = value
        return dic

    def get(
        self, url: Union[WUrl, str], ini: WRequestINI = None, **kwargs
    ) -> WResponse:
        return WResponse(self.session.get(str(url), **self.__dic(ini, **kwargs)))

    def post(
        self,
        url: Union[WUrl, str],
        data=None,
        json=None,
        ini: WRequestINI = None,
        **kwargs,
    ) -> WResponse:
        return WResponse(
            self.session.post(
                str(url), data=data, json=json, **self.__dic(ini, **kwargs)
            )
        )

    def save_cookies_file(self, filename: str):
        with open(filename, "w") as f:
            f.write(json.dumps(dict_from_cookiejar(self.session.cookies)))

    def load_cookies_file(self, filename: str):
        with open(filename, "r") as f:
            self.session.cookies = cookiejar_from_dict(json.loads(f.read()))

    def load_cookies_str(self, cookies_str: str, domain: Union[str, None] = None):
        for cookie in cookies_str.strip().split(";"):
            key, value = cookie.split("=", 1)
            self.session.cookies.set(key.strip(), value.strip(), domain=domain)

    def load_cookie_editor(self, editor_filename: str):
        with open(editor_filename, "rb") as f:
            cookie_json = json.load(f)
        for cookie in cookie_json:
            cookie: dict
            cookie_dic = {}
            translate_dict = {
                "name": "name",
                "value": "value",
                "expirationDate": "expires",
                "domain": "domain",
            }
            for key, value in cookie.items():
                if key in translate_dict:
                    cookie_dic[f[key]] = value
            self.session.cookies.set(**cookie_dic)
