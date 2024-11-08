import threading
import time

WLock = threading.Lock


class WMultiThread:

    def __init__(self, thread_num: int = 8):
        self.thread_num = thread_num
        self._func = None
        self._lock = threading.Lock()
        self._tasks = None
        self._begin_time: int = 0
        self._end_time: int = 0
        self._finished_tasks_num = 0
        self._all_tasks_num = 0
        self._is_running_thread_num = 0
        self._finished_callback_func = None

    def _run_func(self, *args, **kwargs):
        try:
            while not self._func(next(self._tasks), self._lock, *args, **kwargs):
                self._finished_tasks_num += 1
        except StopIteration:
            pass
        self._lock.acquire()
        self._is_running_thread_num -= 1
        self._end_time = time.time()
        self._is_running = False
        if self._finished_callback_func:
            self._finished_callback_func()
            self._finished_callback_func = None
        self._lock.release()

    def run(self, func: callable, tasks: list, *args, **kwargs):
        self._func = func
        self._is_running = True
        self._begin_time = time.time()
        self._finished_tasks_num = 0
        self._all_tasks_num = len(tasks)
        self._is_running_thread_num = self.thread_num
        self._tasks = iter(tasks)
        for i in range(self.thread_num):
            threading.Thread(target=self._run_func, args=args, kwargs=kwargs).start()

    def set_finished_callback_func(self, func: callable):
        self._finished_callback_func = func
    
    @property
    def begin_time(self):
        return self._begin_time

    @property
    def end_time(self):
        return self._end_time

    @property
    def is_running(self):
        return self._is_running_thread_num

    @property
    def progress(self) -> float:
        if self._all_tasks_num == 0:
            return 0.0
        return round(self._finished_tasks_num / self._all_tasks_num, 6)
