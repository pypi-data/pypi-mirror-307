from urllib import parse
from typing import List, Union


class WUrl:
    __scheme: str  # http, https, ftp, file, etc.
    __netloc: str  # domain name or IP address
    __path: str  # path on the server
    __params: str  # parameters for the path
    __query: str  # query string
    __fragment: str  # fragment identifier

    def __init__(self, url: str = ""):
        if isinstance(url, WUrl):
            self.__dict__ = url.__dict__
            return
        parse_result = parse.urlparse(str(url))
        self.__scheme = parse_result.scheme
        self.__netloc = parse_result.netloc
        self.__path = parse_result.path
        self.__params = parse_result.params
        self.__query = parse_result.query
        self.__fragment = parse_result.fragment

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, other) -> bool:
        return str(self) == str(other)

    @property
    def sheme(self) -> str:
        return self.__scheme

    @property
    def netloc(self) -> str:
        return self.__netloc

    @property
    def path(self) -> str:
        return self.__path

    @property
    def params(self) -> str:
        return self.__params

    @property
    def query(self) -> str:
        return self.__query

    @property
    def fragment(self) -> str:
        return self.__fragment

    @property
    def path_list(self) -> List[str]:
        return self.__path.lstrip("/").split("/")

    @property
    def query_dict(self) -> dict:
        return dict(parse.parse_qsl(self.__query))

    @property
    def unquoted_url(self) -> "WUrl":
        return WUrl(parse.unquote(str(self)))

    @property
    def filename(self) -> str:
        return self.path_list[-1]

    def __str__(self) -> str:
        return parse.urlunparse(
            (
                self.__scheme,
                self.__netloc,
                self.__path,
                self.__params,
                self.__query,
                self.__fragment,
            )
        )

    def __repr__(self) -> str:
        return (
            f"WUrl(sheme={self.__scheme}, "
            f"netloc={self.__netloc}, "
            f"path={self.__path}, "
            f"params={self.__params}, "
            f"query={self.__query}, "
            f"fragment={self.__fragment})"
        )

    def __setitem__(self, key: Union[str, int], value: str) -> None:
        if isinstance(key, int):
            path_list = self.path_list
            path_list[key] = value
            self.__path = "/".join(path_list)
        else:
            query_dict = self.query_dict
            query_dict[key] = value
            self.__query = parse.urlencode(query_dict)

    def __delitem__(self, key: Union[str, int]) -> None:
        if isinstance(key, int):
            path_list = self.path_list
            del path_list[key]
            self.__path = "/".join(path_list)
        else:
            query_dict = self.query_dict
            del query_dict[key]
            self.__query = parse.urlencode(query_dict)

    def __getitem__(self, key: Union[str, int]) -> str:
        if isinstance(key, int):
            return self.path_list[key]
        else:
            return self.query_dict[key]

    def join(self, *paths: str) -> "WUrl":
        return WUrl(parse.urljoin(str(self), "/".join(paths)))

    def copy(self) -> "WUrl":
        return WUrl(str(self))
