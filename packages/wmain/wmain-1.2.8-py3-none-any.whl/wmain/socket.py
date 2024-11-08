import socket
import threading
from typing import List, Tuple, Union, Iterator, Dict

class Connect:

    def __init__(self, addr: str, sock: socket.socket):
        self.sock: socket.socket = sock
        self.addr: Tuple[str, int] = addr

    def __str__(self):
        return str(self.addr)
    
    def __repr__(self):
        return f"Connect({self.addr})"
    
    def __del__(self):
        self.sock.close()

    def _recv(self) -> Iterator[str]:
        while 1:
            l = int(self.sock.recv(1024).decode("utf-8"))
            s = self.sock.recv(l).decode("utf-8")
            yield s

    def recv(self) -> Iterator[Union[str, None]]:
        try:
            for s in self._recv():
                yield s
        except Exception:
            self.sock.close()
            yield None

    def send(self, s: str) -> bool:
        try:
            bs = s.encode("utf-8")
            self.sock.send(str(len(bs)).encode("utf-8"))
            self.sock.send(bs)
            return True
        except Exception:
            return False

class Host:
    ip: Union[str, None]
    port: Union[int, None]
    server_sock: socket.socket
    client_sock: Union[socket.socket, None]
    connects: Dict[Tuple[str, int], Connect]
    spipe: List[Tuple[Connect, str]]

    def __init__(self, ip: Union[str, None] = None, port: Union[int, None] = None):
        self.addr = (ip, port)
        self.connects = {}
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.spipe = []

    def __del__(self):
        self.server_sock.close()
        self.client_sock.close()

    def __add_connect(self, connect: Connect) -> bool:
        self.connects[connect.addr] = connect
        threading.Thread(target=self.__recv, args=(connect,)).start()

    def __recv(self, connect: Connect) -> None:
        for msg in connect.recv():
            if msg is None:
                return
            self.spipe.append((connect, msg))

    def __accept(self) -> None:
        while 1:
            try:
                sock, addr = self.server_sock.accept()
                self.__add_connect(Connect(addr, sock))
            except Exception:
                break
    
    def iter_connects(self) -> Iterator[Connect]:
        addrs = list(self.connects.keys()).copy()
        for addr in addrs:
            if addr in self.connects:
                yield self.connects[addr]
    
    def accept(self) -> None:
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.bind(self.addr)
        self.server_sock.listen()
        threading.Thread(target=self.__accept).start()

    def stop_accept(self) -> None:
        self.server_sock.close()

    def connect(self, ip: str, port: int) -> bool:
        try:
            self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_sock.connect((ip, port))
            self.__add_connect(Connect((ip, port), self.client_sock))
            return True
        except Exception:
            return False

    def send_all(self, s: str) -> None:
        for connect in self.iter_connects():
            connect.send(s)

    def send(self, s: str, addr: Union[Tuple[str, int], None] = None) -> None:
        if addr is None:
            self.send_all(s)
        else:
            self.connects[addr].send(s)

    def has_msg(self) -> bool:
        return len(self.spipe) > 0

    def recv_all(self) -> List[Tuple[Connect, str]]:
        ret = self.spipe.copy()
        self.spipe.clear()
        return ret

    def recv(self, index: int = 0) -> Tuple[Connect, str]:
        return self.spipe.pop(index)

    def close(self, addr: Union[Tuple[str, int], None] = None) -> None:
        if addr is None:
            for connect in self.iter_connects():
                connect.sock.close()
            self.connects.clear()
        else:
            self.connects[addr].sock.close()
            self.connects.pop(addr)
