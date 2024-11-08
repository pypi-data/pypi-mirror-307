from requests import Response
import json
import re
from lxml import etree
from lxml.etree import _Element
from typing import List

class WResponse:

    def __init__(self, response: Response) -> None:
        self.response = response
        charset: re.Match = re.search(
            r'charset=["\']?([a-z0-9-]*)["\']?', response.text
        )
        self.response.encoding = (
            charset.group(1) if charset else response.apparent_encoding
        )

    def __repr__(self) -> str:
        return f"<WResponse [{self.status_code}]>"
    
    def __str__(self) -> str:
        return f"<WResponse [{self.status_code}]>"
    
    def xpath(self, xpath: str) -> List[_Element]:
        return etree.HTML(self.text).xpath(xpath)
    
    def xpath_str(self, xpath: str) -> List[str]:
        return [ele.xpath('string(.)') for ele in self.xpath(xpath)]
    
    @property
    def json(self) -> json:
        return self.response.json()
    
    @property
    def status_code(self) -> int:
        return self.response.status_code

    @property
    def content(self) -> bytes:
        return self.response.content

    @property
    def text(self) -> str:
        return self.response.text

    @property
    def headers(self) -> dict:
        return self.response.headers

    @property
    def cookies(self) -> dict:
        return self.response.cookies

    @property
    def url(self) -> str:
        return self.response.url

    @property
    def encoding(self) -> str:
        return self.response.encoding

    @property
    def is_redirect(self) -> bool:
        return self.response.is_redirect

    @property
    def history(self) -> list:
        return self.response.history
    
    def save(self, filename: str) -> None:
        with open(filename, 'wb') as f:
            f.write(self.content)
