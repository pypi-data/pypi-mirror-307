"""
云码接口
# 数英汉字类型
# 通用数英1-4位 10110
# 通用数英5-8位 10111
# 通用数英9~11位 10112
# 通用数英12位及以上 10113
# 通用数英1~6位plus 10103
# 定制-数英5位~qcs 9001
# 定制-纯数字4位 193
# 中文类型
# 通用中文字符1~2位 10114
# 通用中文字符 3~5位 10115
# 通用中文字符6~8位 10116
# 通用中文字符9位及以上 10117
# 定制-XX西游苦行中文字符 10107
# 计算类型
# 通用数字计算题 50100
# 通用中文计算题 50101
# 定制-计算题 cni 452
"""

# {"msg":"识别成功","code":10000,"data":{"code":0,"data":"2812","time":0.032166481018066406,"unique_code":"368e806b00cc397f330cf0f75ae2979f"}}
from wmain.requests import WSession
from wmain.exceptions import CaptchaException
import base64
import os


class CloudCodeClient:
    """
    云码通用连接
    """

    def __init__(self, token):
        self.url = "http://api.jfbym.com/api/YmServer/customApi"
        self.session = WSession()
        self.session.ini.headers["Content-Type"] = "application/x-www-form-urlencoded"
        self.token = token

    def CommonPost(self, base64_str, type_):
        self.data = {"image": base64_str, "token": self.token, "type": type_}
        resp = self.session.post(self.url, data=self.data)
        return resp.json

    def _Post4LPic_by_base64(self, base64_str):
        return self.CommonPost(base64_str, "10110")

    def _Post4LPic(self, img_file):
        with open(img_file, "rb") as f:
            return self._Post4LPic_by_base64(base64.b64encode(f.read()).decode())


class CloudCode_Api(CloudCodeClient):

    def __init__(self):
        super().__init__("3GaQwdwSBe0Zwv-XpZ7UXiT1nGHDzhsbn2IzBzDp9os")

    def __GetCaptcha(self, json_data: dict) -> str:
        try:
            return json_data["data"]["data"]
        except TypeError:
            raise CaptchaException("识别失败")

    def Post4(self, img_file: str):
        return self.__GetCaptcha(self._Post4LPic(img_file))

    def Post4_by_base64(self, base64_str: str):
        return self.__GetCaptcha(self._Post4LPic_by_base64(base64_str))

    def Post4_by_bytes(self, img_bytes: bytes):
        base64_str = base64.b64encode(img_bytes)
        return self.__GetCaptcha(self._Post4LPic_by_base64(base64_str))


api_cloudcode = CloudCode_Api()
