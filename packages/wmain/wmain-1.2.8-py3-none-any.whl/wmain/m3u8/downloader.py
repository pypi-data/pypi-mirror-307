from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from typing import List, Union
import os

from wmain.thread import WMultiThread, WLock
from wmain.m3u8.paser import WParser, _M3U8VideoList
from wmain.base import create_dir
from wmain.requests.session import WSession
from wmain.requests.url import WUrl


class M3U8DownloadTask:
    url: WUrl
    key: Union[None, bytes]
    iv: Union[None, bytes]
    session: WSession
    file_path: str

    def __init__(self, url, key, iv, session, file):
        self.url = url
        self.key = key
        self.iv = iv
        self.session = session
        self.file_path = file

    def do(self, overwrite: bool = False):
        if (
            not overwrite
            and os.path.exists(self.file_path)
            and os.path.getsize(self.file_path) > 0
        ):
            return
        data = self.session.get(self.url).content
        if self.key:
            cryptor: AES = AES.new(self.key, AES.MODE_CBC, IV=bytes(self.iv))
            plain_text = cryptor.decrypt(pad(data, 16))
            data = plain_text.rstrip(b"\0")
        with open(self.file_path, "wb") as f:
            f.write(data)


class WDownloader:
    res: WParser
    tasks: List[M3U8DownloadTask]
    thread: WMultiThread
    _mp4_file: str
    _ts_dir: str

    def __init__(
        self, m3u8_res: WParser, dir_path: str, mp4_name: str, thread_num: int = 8
    ):
        self.tasks = []
        self.thread = WMultiThread(thread_num)
        self.res = m3u8_res
        self._ts_dir = os.path.join(dir_path, "ts")
        create_dir(self._ts_dir)
        self._mp4_file = os.path.join(dir_path, mp4_name.replace(".mp4", "") + ".mp4")
        open(self._mp4_file, "wb").close()
        self.flush_tasks()

    def flush_tasks(self, filter_func: Union[None, callable] = None):
        self.tasks.clear()
        for video_list in self.res.video_lists:
            video_list: _M3U8VideoList
            if filter_func and filter_func(video_list):
                continue
            for index, url in enumerate(video_list.url_list):
                self.tasks.append(
                    M3U8DownloadTask(
                        url,
                        video_list.key,
                        video_list.iv,
                        self.res.session,
                        os.path.join(f"{self._ts_dir}", f"{index}.ts"),
                    )
                )

    def _do_task(self, task: M3U8DownloadTask, lock: WLock, overwrite: bool = False):
        task.do(overwrite)

    def start(self, overwrite: bool = False):
        self.thread.set_finished_callback_func(self.merge)
        self.thread.run(self._do_task, self.tasks, overwrite)

    def merge(self):
        with open(self._mp4_file, "ab") as mp4_f:
            ts_files = os.listdir(self._ts_dir)
            ts_files.sort(key=lambda x: int(x.split(".")[0]))
            for ts_file in ts_files:
                file_path = os.path.join(self._ts_dir, ts_file)
                with open(file_path, "rb") as ts_f:
                    mp4_f.write(ts_f.read())
        os.rename(self._mp4_file, self._mp4_file.replace(".mp4", ".ts"))