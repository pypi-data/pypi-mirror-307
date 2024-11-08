from typing import List, Dict, Union

from wmain.requests.url import WUrl
from wmain.requests.session import WSession

EXT_KEY = "#EXT-X-KEY"
EXT_INF = "#EXTINF"  #
EXT_VIDEO = "#EXT-X-VIDEO"  # default tag, not in m3u8 standard
EXT_DISCONTINUITY = "EXT-X-DISCONTINUITY"
EXT_END = "#EXT-X-ENDLIST"
EXT_SEQUENCE = "#EXT-X-MEDIA-SEQUENCE"
EXT_STREAM_INF = "#EXT-X-STREAM-INF"


class _M3U8Union:

    basic_tag: str = "#EXT-X-VIDEO"
    attrs: List[str] = []

    def __init__(self, m3u8_line: str):
        m3u8_line = m3u8_line.strip()
        if m3u8_line.startswith("#"):
            if ":" not in m3u8_line:
                m3u8_line += ":"
            self.basic_tag, attrs_ = m3u8_line.split(":")
        else:
            attrs_ = m3u8_line
        self.attrs = [attr for attr in attrs_.split(",") if attr]
        self.attrs_dict = dict(attr.split("=") for attr in self.attrs if "=" in attr)

    def __str__(self):
        return f"{self.basic_tag}:{','.join(self.attrs)}"

    def __repr__(self):
        return f"Union(basic_tag='{self.basic_tag}', attrs={self.attrs})"


class _M3U8VideoList:
    method: Union[None, str]
    key: Union[None, bytes]
    url_list: List[str]
    iv: Union[None, bytes]

    def __init__(self):
        self.method = None
        self.key = None
        self.url_list = []
        self.iv = None

    def __str__(self):
        return self.url_list

    def __repr__(self):
        return f"M3U8VideoList(method='{self.method}', key_url='{self.key_url}', key='{self.key}', url_list={self.url_list}, iv='{self.iv}')"


class WParser:

    __caches: Dict[str, List[List[str]]]
    __all_time: float
    unions: List[_M3U8Union]
    m3u8_url: WUrl
    session: WSession

    def __init__(
        self, m3u8_url: Union[str, WUrl] = WUrl(), session: WSession = WSession()
    ):
        self.__caches = {}
        self.__all_time = 0
        self.session = session
        self.unions = []
        self.m3u8_url = WUrl(m3u8_url)

    def __getitem__(self, tag: str) -> List[List[str]]:
        if tag in self.__caches.keys():
            return self.__caches[tag]
        self.__caches[tag] = []
        for i in self.unions:
            if i.basic_tag == tag:
                self.__caches[tag].append(i.attrs)
        return self.__caches[tag]

    def _m3u8_parse(self, m3u8_text: str):
        self.__caches.clear()
        self.unions = [
            _M3U8Union(line) for line in m3u8_text.split("\n") if line.strip()
        ]
        self.__all_time: float = sum([float(i[0]) for i in self[EXT_INF]])

    def parse_m3u8_by_session(self):
        self._m3u8_parse(self.session.get(self.m3u8_url).text)

    def parse_m3u8_by_str(self, m3u8_text: str = None):
        self._m3u8_parse(m3u8_text)

    def parse_m3u8_by_file(self, m3u8_file_path: str = None):
        with open(m3u8_file_path, "r") as f:
            self._m3u8_parse(f.read())

    def try_to_next_level(self, stream_url_index: int = 0):
        next_level_urls = self.next_level_urls
        if next_level_urls:
            next_level_url = next_level_urls[stream_url_index]
            self.m3u8_url = WUrl(next_level_url)
            self.parse_m3u8_by_session()

    @property
    def next_level_urls(self) -> List[str]:
        if not self[EXT_STREAM_INF]:
            return []
        return [self.m3u8_url.join(url[0]) for url in self[EXT_VIDEO]]

    @property
    def all_time(self) -> float:
        return self.__all_time

    @property
    def video_lists(self) -> List[_M3U8VideoList]:
        r = []
        sequence = None
        video_list: _M3U8VideoList = _M3U8VideoList()
        for union in self.unions:
            if union.basic_tag == EXT_KEY:
                attrs = union.attrs_dict
                video_list.iv = sequence
                if "METHOD" in attrs:
                    video_list.method = attrs["METHOD"]
                if "URI" in attrs:
                    video_list.key = self.session.get(
                        self.m3u8_url.join(attrs["URI"])
                    ).content
                    if len(video_list.key) != 16:
                        raise ValueError(
                            f"Key length should be 16, but got {len(video_list.key)}: {video_list.key}"
                        )
                if "IV" in attrs:
                    bs = bytes.fromhex(attrs["IV"].replace("0x", ""))
                    if len(bs) != 16:
                        raise ValueError(
                            f"IV length should be 16, but got {len(bs)}: {bs}"
                        )
                    video_list.iv = bs
            elif union.basic_tag == EXT_VIDEO:
                video_list.url_list.append(self.m3u8_url.join(union.attrs[0]))
            elif union.basic_tag == EXT_DISCONTINUITY or union.basic_tag == EXT_END:
                r.append(video_list)
                video_list = _M3U8VideoList()
                sequence = None
            elif union.basic_tag == EXT_SEQUENCE:
                sequence = union.attrs[0]
        return r
