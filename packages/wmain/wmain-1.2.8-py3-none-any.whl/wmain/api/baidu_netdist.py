from typing import List, Union
import re

from wmain.time import get_timestamp13
from wmain.requests import WSession, WUrl
from wmain.api import api_cloudcode


class _BaiduNetdistF:
    path: str
    name: str
    isdir: bool
    size: int
    fs_id: int

    def __init__(self, bd_file):
        self.bd_file = bd_file
        self.path = bd_file["path"]
        self.name = self.path.split("/")[-1]
        self.isdir = bool(bd_file["isdir"])
        self.size = 0 if self.isdir else bd_file["size"]
        self.fs_id = bd_file["fs_id"]

    def __repr__(self) -> str:
        return self.path

    def __str__(self) -> str:
        return self.path

    def __eq__(self, value: Union[str, "_BaiduNetdistF"]) -> bool:
        if isinstance(value, _BaiduNetdistF):
            return self.name == value.name
        elif isinstance(value, str):
            if value.startswith("/"):
                return self.path == value
            else:
                return self.name == value


class WBaidu_Netdisk:
    session: WSession
    list_url: str = "https://pan.baidu.com/api/list"
    filemanager_url: str = "https://pan.baidu.com/api/filemanager"
    create_url: str = "https://pan.baidu.com/api/create"
    template_variable_url: str = "https://pan.baidu.com/api/gettemplatevariable"
    verify_url: str = "https://pan.baidu.com/share/verify"
    transfer_url: str = "https://pan.baidu.com/share/transfer"
    search_url: str = "https://pan.baidu.com/api/search"

    api_create_url_v2 = "https://pan.baidu.com/rest/2.0/doc/file"

    def __init__(self, cookie_file: str = None, session: WSession = WSession()):
        self.session = session
        if cookie_file is not None:
            self.session.load_cookie_editor(cookie_file)
        self.field = {"bdstoken": None, "token": None}  # 请求需要的域

    def login(self, cookies_str: str):
        self.session.load_cookies_str(cookies_str, ".pan.baidu.com")
        self.init()

    def init(self):
        params = {"fields": '["bdstoken","token"]'}
        dic = self.session.get(self.template_variable_url, params=params).json["result"]
        self.field["token"] = dic["token"]
        self.field["bdstoken"] = dic["bdstoken"]

    def list_iter(self, dir: str, page=1, page_num=1000) -> List[_BaiduNetdistF]:
        resp = self.session.get(
            self.list_url, params={"dir": dir, "num": str(page_num), "page": str(page)}
        )
        return [_BaiduNetdistF(dic) for dic in dict(resp.json)["list"]]

    def list_all(self, dir: str, page_num=1000) -> List[_BaiduNetdistF]:
        r = []
        page = 1
        while 1:
            last_r_size = len(r)
            r += self.list_iter(dir, page, page_num)
            if len(r) - last_r_size < page_num:
                break
            page += 1
        return r

    def del_list(self, file_dir_list: List[str]) -> Union[bool, int]:
        del_list_str = '["' + '","'.join(file_dir_list) + '"]'
        params = {
            "bdstoken": self.field["bdstoken"],
            "async": len(file_dir_list),
            "onnest": "fail",
            "opera": "delete",
        }
        data = {"filelist": del_list_str}
        resp = self.session.post(self.filemanager_url, params=params, data=data)
        errno = resp.json["errno"]
        if errno == 0:
            return True
        else:
            return errno

    def exist(self, file_dir: str, isdir: bool = True) -> bool:
        for file in self.list_all("/" + "/".join(file_dir.split("/")[:-1])):
            if isdir == file.isdir and file == file_dir:
                return True
        return False

    def create_dir(self, dir: str, overwrite: bool = False) -> Union[bool, dict]:
        params = {"bdstoken": self.field["bdstoken"]}
        data = {"path": dir, "isdir": "1", "block_list": "[]"}
        if not overwrite and self.exist(dir, True):
            return "Directory already exists."
        resp = self.session.post(self.create_url, params=params, data=data)
        if resp.json["errno"] == 0:
            return True
        else:
            return resp.json

    def search_iter(
        self, keyword: str, page: int = 1, page_num: int = 1000
    ) -> List[_BaiduNetdistF]:
        page = 1
        params = {
            "order": "time",
            "num": str(page_num),
            "page": str(page),
            "recursion": "1",
            "key": keyword,
        }
        resp = self.session.get(self.search_url, params=params)
        return [_BaiduNetdistF(dic) for dic in resp.json["list"]]

    def search_all(self, keyword: str, page_num: int = 1000) -> List[_BaiduNetdistF]:
        r = []
        page = 1
        while 1:
            last_r_size = len(r)
            r += self.search_iter(keyword, page, page_num)
            if len(r) - last_r_size < page_num:
                break
            page += 1
        return r

    def __verify(self, verify_params, verify_data) -> bool:
        count = 0
        while 1:
            # 开始请求安全api
            # 百度设计了防盗链, 必须有referer
            resp = self.session.post(
                self.verify_url, params=verify_params, data=verify_data
            )
            error = resp.json["errno"]
            if error == 0:
                return True
            elif error == -62:
                captcha_url: str = self.session.get(
                    "https://pan.baidu.com/api/getcaptcha?prod=shareverify"
                ).json["vcode_img"]
                vcode_str = captcha_url.split("?")[1]
                if count > 5:
                    return False
                vcode = api_cloudcode.Post4_by_bytes(
                    self.session.get(captcha_url).content
                )
                verify_params["t"] = get_timestamp13()
                verify_data["vcode"] = vcode
                verify_data["vcode_str"] = vcode_str
                count += 1
            else:
                return False

    def auto_save(
        self, url: Union[str, WUrl], dir="/auto_get", pwd="", verify=True
    ) -> Union[str, dict]:
        url = str(url)
        if not url.startswith("https://pan.baidu.com/s/"):
            return "百度网盘url格式错误"
        resp = self.session.get(url)
        self.session.ini.headers["Referer"] = url
        keyword_list = [
            "分享的文件已经被删除",
            "分享的文件已经被取消",
            "因为涉及侵权、色情、反动、低俗等信息，无法访问",
            "链接错误没找到文件",
            "分享文件已过期",
        ]
        for keyword in keyword_list:
            if keyword in resp.text:
                return keyword
        if verify:
            url = resp.url
            url_ = WUrl(url)
            url_query = url_.query_dict
            surl = url_[1] if "surl" not in url_query else url_query["surl"]
            if "pwd" in url_query and pwd == "":
                pwd = url_query["pwd"]
            verify_params = {
                "t": get_timestamp13(),
                "surl": surl,
                "bdstoken": self.field["bdstoken"],
            }
            verify_data = {"pwd": pwd, "vcode": "", "vcode_str": ""}
            if not self.__verify(verify_params, verify_data):
                return "安全验证失败"

        resp = self.session.get(url)
        share_uk = re.findall('share_uk:"([0-9]*)"', resp.text)[0]
        share_id = re.findall('shareid:"([0-9]*)"', resp.text)[0]
        fs_id = re.findall('"fs_id":([0-9]*),', resp.text)[0]
        transfer_params = {"shareid": share_id, "from": share_uk, "ondup": "newcopy"}
        transfer_data = {
            "fsidlist": f"[{fs_id}]",
            "path": dir,
        }
        resp = self.session.post(
            self.transfer_url, params=transfer_params, data=transfer_data
        )
        if resp.json["errno"] == 0:
            result = resp.json["extra"]["list"][0]
            return f'成功保存到{result["to"]}'
        else:
            return resp.json
